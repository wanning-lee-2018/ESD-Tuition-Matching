import requests
import json
############################READ#########################################
#--------------WHAT DOES THIS FILE DO?-------------------------
# It will print out your telegram chat id, which is needed for our telegram bot to send messages to you
#step 1: find our telegram bot on telegram and type any message in the texbox and send the message

# Here is the link to our telegram bot: http://t.me/tuitionmatch_bot

#step 2: Navigate to the directory containing this file and run this file in the command prompt using "python telebot.py"
#step 3: your telegram chat id will be printed out, please verify against the telegram username and first name
#that is also printed to ensure that telegram chat id is yours

#If error is printed in the command prompt console, repeat step 1-2 again

# Here is the link to the official telegram API documentation:
# https://core.telegram.org/bots/api#available-methods

###########################CODE#####################################
#tele_url=https://api.telegram.org/bot<token>/METHOD_NAME

#please keep the telegram bot token secret
telebot_token='<telegrambot token>'#Change to your own telegrambot token

#telegram base url
tele_base_url='https://api.telegram.org/bot{}/'.format(telebot_token)

# get Updates method
getteleuserinfo_url=tele_base_url + 'getUpdates'


def get_teleuser_info():
    # params={'offset':-1}
    # r=requests.get(getteleuserinfo_url,params=params)
    r=requests.get(getteleuserinfo_url,)
    tele_chat_id=r.json()['result'][-1]['message']['chat']['id']
    tele_username=r.json()['result'][-1]['message']['chat']['username']
    tele_firstname=r.json()['result'][-1]['message']['chat']['first_name']
    # result=json.dumps(r.json(),indent=2)
    # return result
    result={"Your Telegram chat id": tele_chat_id,"Your Telegram username":tele_username,"Your Telegram firstname":tele_firstname}
    return result

teleuser_info=get_teleuser_info()
print(teleuser_info)
#print out your telegram chat id, which is needed for our telegram bot to send messages to you


############################################################









