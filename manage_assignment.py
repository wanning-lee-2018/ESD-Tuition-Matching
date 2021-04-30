from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ

import requests
from invokes import invoke_http

# from tuitionbot import send_tutee_msg,send_tutor_msg
# from emailbot import send_tutor_email,send_tutee_email

import amqp_setup 
# i have to comment this out to run this
import pika
import json

app = Flask(__name__)
CORS(app)

# Must rmb to change the port accordingly
tutee_URL =environ.get('tutee_URL')
#  or "http://localhost:5000/tutee"
assignment_URL =environ.get('assignment_URL')
#  or "http://localhost:5001/assignment"
tutor_URL =environ.get('tutor_URL')
#  or "http://localhost:5002/tutor"

# USER SCENARIO 1 - TUTEE POST TUITION ASSIGNMENT

#for error and activity handling checks for code 

# @app.route("/manage_assignment", methods=['POST'])
# def check_code():
    
#     if code not in range(200,300):
#         print('\n\n')

# Check if input information is JSON
@app.route("/manage_assignment/post/<string:TuteeID>", methods=['POST'])
def post_assignment(TuteeID):
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            tutee_input = request.get_json()

            # Merge tutee_input with TuteeID
            assignment = {'TuteeID': TuteeID, 'tutee_input': tutee_input}
            print("\nReceived an assignment in JSON:", assignment)

            # do the actual work
            # 1. Send asssignment info {assignment_details}
            result = process_PostAssignment(assignment)
            return jsonify(result), 200

        except Exception as e:
            pass  # do nothing.

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

# POST assignment to assignment microservice
def process_PostAssignment(assignment):
    # Send the assignment info
    # Invoke the assignment microservice
    postAsgmt_URL = assignment_URL + "/post" 
    print(postAsgmt_URL)
    print('\n-----Invoking assignment microservice-----')
    assignment_result = invoke_http(postAsgmt_URL, method='POST', json=assignment)
    print('assignment_result:', assignment_result)

    # Return created assignment
    return {
        "code": 201,
        "data": {
            "assignment_result": assignment_result
        }
    }

# USER SCENARIO 2.1 - TUTOR VIEW ALL OPEN TUITION ASSIGNMENT WITH TUTEE GRADE, GENDER & LOCATION
@app.route("/manage_assignment")
def view_all_assignment():
    # Get all open assignment from assignment microservice
    # Invoke the assignment microservice
    print('\n-----Invoking assignment microservice-----')
    assignment_result = invoke_http(assignment_URL, method='GET', json=None)
    print('assignment_result:', assignment_result)

    # Return all open assignments
    return {
        "code": 200,
        "data": {
            "assignment_result": assignment_result,
        }
    }

# USER SCENARIO 2.2 - TUTOR VIEW TUTEE’S INFORMATION
# GET TuteeID from assignment microservice
@app.route("/manage_assignment/getTuteeDetails/<string:AssignmentID>")
def get_TuteeID(AssignmentID): 
    # Get TutorID
    # Invoke the assignment microservice
    print('\n-----Invoking assignment microservice-----')
    assignment_info_url=assignment_URL+'/'+ AssignmentID
    print(assignment_info_url)
    assignment_info_result = invoke_http(assignment_info_url, method='GET', json=None)
    print('assignment_info_result:', assignment_info_result)

    TuteeID_result=assignment_info_result["data"]["TuteeID"]
    print(TuteeID_result)
    tutee_info = get_tuteeInfo(TuteeID_result)
    return jsonify(tutee_info), 200

# GET tutee information from tutee microservice
def get_tuteeInfo(TuteeID_result): 
    # Get tutee info
    # Invoke the tutee microservice
    print('\n-----Invoking tutee microservice-----')
    tutee_info_url=tutee_URL+'/'+ str(TuteeID_result)
    print(tutee_info_url)
    tutee_result = invoke_http(tutee_info_url, method='GET', json=None)
    print('tutor_result:', tutee_result)

    return {
        "code": 200,
        "data": {
            "tutee_result": tutee_result
        }
    }

# USER SCENARIO 3 - TUTOR APPLIES FOR TUITION ASSIGNMENT
@app.route("/manage_assignment/apply/<string:TutorID>/<string:TuteeID>/<string:AssignmentID>", methods=['PUT'])
def apply_tuition(TutorID,TuteeID,AssignmentID,):
    #proceed to updating the assignment status to pending
    assignment_update_url=assignment_URL+'/'+ AssignmentID
    update_status={"Status":"Pending","TutorID":TutorID}
    print(update_status)
    print('\n\n-----Invoking Assignment microservice-----')
    assignment_result = invoke_http(
        assignment_update_url, method="PUT", json=update_status)
    print("assignment_result:", assignment_result, '\n')
    # Check the assignment update result; 
    code = assignment_result["code"]
    if code not in range(200, 300):
    #Return error
        return assignment_result
    
    #getting tutee's telegram chatID and sending notification to them
    assignment_TimePosted=assignment_result["data"]["TimePosted"]
    tutee_tele_url=tutee_URL+'/'+ TuteeID
    print('\n\n-----Invoking Tutee microservice-----')
    tutee_result = invoke_http(
        tutee_tele_url, method="GET", json=None)
    print("tutee_result:", tutee_result, '\n')

    TuteeTeleChatID=tutee_result["data"]["TuteeTeleChatID"]
    
    # send_tutee_msg(TuteeTeleChatID,msg)

    # EMAIL
    TuteeEmail=tutee_result["data"]["TuteeEmail"]
    
    # send_tutee_email(TuteeEmail,EmailMsg)

    msg="A tutor with id {} just applied for the tuition assignment with id {} which you have posted on {}".format(TutorID,AssignmentID,assignment_TimePosted)
    
    #AMQP to sendgri api
    sendemail_result={"TuteeEmail":TuteeEmail,"EmailMsg":msg}
    message = json.dumps(sendemail_result)
    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="notification.Tutorapply", 
        body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
    # make message persistent within the matching queues until it is received by some receiver 
    # (the matching queues have to exist and be durable and bound to the exchange)
    #AMQP to telegram api(send notification to tutee) 
    sendtele_result={"TuteeTeleChatID":TuteeTeleChatID,"TeleMsg":msg}
    message = json.dumps(sendtele_result)
    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="notification.Tutorapply", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        # make message persistent within the matching queues until it is received by some receiver 
        # (the matching queues have to exist and be durable and bound to the exchange)

    #==========================
    return {
        "assignment_result": assignment_result
    }

# USER SCENARIO 4.1 - TUTEE VIEW POSTED TUITION ASSIGNMENTS AND
# TUTEE REVIEW TUTOR'S DETAILS
@app.route("/manage_assignment/all/<string:TuteeID>")
def get_all_posted_asgmt(TuteeID):
    # Invoke the assignment microservice
    print('\n-----Invoking assignment microservice-----')
    posted_asgmt_URL = assignment_URL + "/all/" + TuteeID
    posted_asgmt_result = invoke_http(posted_asgmt_URL, method='GET', json=None)
    print('posted_asgmt_result:', posted_asgmt_result)

    # print(posted_asgmt_result.data.assignments.TutorID)
    # tutor_asgmt_URL = tutor_URL + "/" + str(tutorID)

    # Return all posted assignments
    return {
        "code": 200,
        "data": {
            "posted_asgmt_result": posted_asgmt_result
        }
    }

# GET TutorID from assignment microservice
@app.route("/manage_assignment/<string:AssignmentID>")
def get_TutorID(AssignmentID): 
    # Get TutorID
    # Invoke the assignment microservice
    print('\n-----Invoking assignment microservice-----')
    assignment_info_url=assignment_URL+'/'+ AssignmentID
    print(assignment_info_url)
    assignment_info_result = invoke_http(assignment_info_url, method='GET', json=None)
    print('assignment_info_result:', assignment_info_result)

    # code = TutorID_result["code"]
    # if code not in range(200, 300):
    # #Return error
    #     return TutorID_result
    TutorID_result=assignment_info_result["data"]["TutorID"]
    print(TutorID_result)
    tutor_info = get_tutorInfo(TutorID_result)
    return jsonify(tutor_info), 200

# GET tutor information from tutor microservice
def get_tutorInfo(TutorID_result): 
    # Get tutor info
    # Invoke the tutor microservice
    print('\n-----Invoking tutor microservice-----')
    tutor_info_url=tutor_URL+'/'+ str(TutorID_result)
    tutor_result = invoke_http(tutor_info_url, method='GET', json=None)
    print('tutor_result:', tutor_result)
    # code = tutor_result["code"]
    # if code not in range(200, 300):
    # #Return error
    return {
        "code": 200,
        "data": {
            "tutor_result": tutor_result
        }
    }

# USER SCENARIO 4.2 - TUTEE ACCEPTS/REJECTS TUTOR
@app.route("/manage_assignment/match/<string:TutorID>/<string:TuteeID>/<string:AssignmentID>", methods=['PUT'])
def match_tuition(TutorID,TuteeID,AssignmentID):
    #checks reject or accept
    data = request.get_json()
    #update status to the assignment microservice
    #invoke assignment microservice(PUT method)
    # Invoke the assignment microservice
    print('\n-----Invoking assignment microservice-----')
    assignment_update_url=assignment_URL+'/'+ AssignmentID
    json_status={"Status": data['Status']}
    assignment_result = invoke_http(assignment_update_url, method='PUT', json=json_status)
    print('assignment_result:', assignment_result)
    # Check the assignment update result; 
    code = assignment_result["code"]
    if code not in range(200, 300):
    #Return error
        return assignment_result
        #if no error while invoking assignment microservice
    tutor_contact_url=tutor_URL+'/'+ TutorID
    print('\n\n-----Invoking Tutor microservice-----')
    tutor_result = invoke_http(
        tutor_contact_url, method="GET", json=None)
    print("tutor_result:", tutor_result, '\n')

    TutorTeleChatID=tutor_result["data"]["TutorTeleChatID"]
    TutorEmail=tutor_result["data"]["TutorEmail"]
    print(TutorEmail)
    
    if data['Status']=='Rejected':
        # What should the message contain? dear [tutor's Name]? tuition assignment info
        msg="Your application for tuition assignment with ID {} has been rejected by the tutee. Please try applying for other tuition assignments,thank you.".format(AssignmentID)
        # send_tutor_msg(TutorTeleChatID,msg)

        #EMAIL
        # send_tutor_email(TutorEmail,EmailMsg)
        #AMQP to sendgrid api
        sendemail_result={"TutorEmail":TutorEmail,"EmailMsg":msg}
        message = json.dumps(sendemail_result)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="notification.tuteerejectstutor", 
        body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

         #AMQP to telegram api(send notification containing only message to tutor)
        sendtele_result={"TutorTeleChatID":TutorTeleChatID,"Telemsg":msg}
        message = json.dumps(sendtele_result)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="notification.tuteerejectstutor", 
                body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        return assignment_result
        
    #return assignment result + confirmation message
    elif data['Status']=='Accepted':
        #inform tutor of accepted tuition assignment, ask them to retrieve tutee's contact info on the website
        # What should the message contain? dear [tutor's Name]? tuition assignment info, tutee's details?
        msg="Your application for tuition assignment with ID {} has been accepted by the tutee. Please check the website for tutee's contact details.Thank you.".format(AssignmentID)
        # send_tutor_msg(TutorTeleChatID,msg)
        #AMQP to telegram api(send notification containing tutee contact info to tutor)
        sendtele_result={"TutorTeleChatID":TutorTeleChatID,"Telemsg":msg}
        message = json.dumps(sendtele_result)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="notification.tuteeacceptstutor", 
                body=message, properties=pika.BasicProperties(delivery_mode = 2))
        #EMAIL
        # send_tutor_email(TutorEmail,EmailMsg)
        #AMQP to sendgrid api
        sendemail_result={"TutorEmail":TutorEmail,"EmailMsg":msg}
        message = json.dumps(sendemail_result)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="notification.tuteeacceptstutor", 
        body=message, properties=pika.BasicProperties(delivery_mode = 2))
        
        #retrieve tutor contact info and send back to web UI to tutee
        TutorPhone=tutor_result["data"]["TutorPhone"]
        TutorName=tutor_result["data"]["TutorName"]
        TutorTelegramID=tutor_result["data"]["TutorTelegramID"]
        tutor_contact={"TutorName":TutorName,"TutorPhone":TutorPhone,"TutorTelegramID":TutorTelegramID}
        return tutor_contact

# USER SCENARIO 5 - TUTOR CHECKS DETAILS OF ACCEPTED ASSIGNMENT
@app.route("/manage_assignment/accepted/<string:TutorID>")
def get_accepted_assignment(TutorID):
    # Get assignment info
    # Invoke the assignment microservice
    print('\n-----Invoking assignment microservice-----')
    assignment_update_URL = assignment_URL + "/accepted/" + TutorID
    print(assignment_update_URL)
    accepted_assignment = invoke_http(assignment_update_URL, method='GET', json=None)
    print('accepted_assignment:', accepted_assignment)

    accepted = accepted_assignment["data"]["assignments"]
    list_of_tuteeID = []
    for a in accepted:
        list_of_tuteeID.append(a["TuteeID"])

    print(list_of_tuteeID)

    list_of_tuteeInfo = []
    for i in list_of_tuteeID:
        print('\n-----Invoking tutee microservice-----')
        tutee_update_URL = tutee_URL + "/" + str(i)
        print(tutee_update_URL)
        accepted_tutee_info = invoke_http(tutee_update_URL, method='GET', json=None)
        list_of_tuteeInfo.append(accepted_tutee_info)
        print('list_of_tuteeInfo:', list_of_tuteeInfo)

    # Return accepted assignment information
    return {
        "code": 200,
        "data": {
            "accepted_assignment": accepted_assignment,
            "list_of_tuteeInfo": list_of_tuteeInfo
        }
    }

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for managing assignments...")
    app.run(host="0.0.0.0", port=5100, debug=True)
    # Notes for the parameters:
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program,
    #       and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.
