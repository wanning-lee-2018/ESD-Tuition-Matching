#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import json
import os
import requests
import amqp_setup
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

monitorBindingKey='notification.*'




#############################READ############################################

#---------------------------Telegram-----------------------------------------
#please keep the telegram bot token secret
telebot_token='<telegrambot token>'#Change to your own telegrambot token

#telegram base url
tele_base_url='https://api.telegram.org/bot{}/'.format(telebot_token)
# send message method
sendtelemsg_url=tele_base_url + 'sendMessage'


# Here is the link to the official telegram API documentation:
# https://core.telegram.org/bots/api#available-methods
#------------------------SendGrid--------------------------------------------
sg = SendGridAPIClient('<SendGrid API key>') #input your SendGrid API key here

#Here is the link to the official sendgrid API documentation
#https://sendgrid.com/docs/api-reference/

#####################################CODE######################################

def receivenotification():
    amqp_setup.check_setup()
        
    queue_name = 'Notification'
    
    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived an telegram notification from " + __file__)
    processmsg(json.loads(body))
    print() # print a new line feed

def processmsg(msg):
    if "TutorTeleChatID" in msg:
            params={'chat_id':msg["TutorTeleChatID"],'text':msg["TeleMsg"]}
            r=requests.post(sendtelemsg_url,params=params)
            print(r.status_code)
            return None
    if "TuteeTeleChatID" in msg :
        params={'chat_id':msg["TuteeTeleChatID"],'text':msg["TeleMsg"]}
        r=requests.post(sendtelemsg_url,params=params)
        print(r.status_code)
        return None


    if "TutorEmail" in msg:
        message = Mail(
        from_email='<Sender email address>', #input sender email address here (for sending our the notification)
        to_emails=msg["TutorEmail"],
        subject='Alert Status Updated',
        html_content='<p>' + msg["EmailMsg"] +'</p>')
        try:
            # sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e)
        return None

    if "TuteeEmail" in msg:
        message = Mail(
        from_email='<Sender email address>', #input sender email address here (for sending our the notification)
        to_emails=msg["TuteeEmail"],
        subject='Alert Tutor Application',
        html_content='<p>' + msg["EmailMsg"] +'</p>')
        try:
            # sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e)
        return None

    print("Recording a msg:")
    print(msg)

if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receivenotification()










