#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import os
from os import environ
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
#take note of your mysql server port number(3306 or 3308)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
#  or 'mysql+mysqlconnector://root@localhost:3306/assignment'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)
CORS(app)

class Assignment(db.Model):
    __tablename__ = 'assignment'

    AssignmentID = db.Column(db.Integer, primary_key=True)
    TuteeID = db.Column(db.Integer, nullable=False)
    TutorID = db.Column(db.Integer, nullable=True)
    Status = db.Column(db.String(10), nullable=False)
    AssignmentDayTime=db.Column(db.String(32), nullable=False)
    Subject=db.Column(db.String(32), nullable=False)
    Rate = db.Column(db.Float(precision=2), nullable=False)
    TimePosted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    TimeLastModified = db.Column(db.DateTime, nullable=True,
                         default=datetime.now, onupdate=datetime.now)
        

    def json(self):
        dto = {
            'AssignmentID': self.AssignmentID,
            'TuteeID': self.TuteeID,
            'TutorID': self.TutorID,
            'Status': self.Status,
            'AssignmentDayTime': self.AssignmentDayTime,
            'Subject': self.Subject,
            'Rate': self.Rate,
            'TimePosted': self.TimePosted,
            'TimeLastModified': self.TimeLastModified
        }
        return dto

#USER SCENARIO 1: Tutee post assignments
@app.route("/assignment/post", methods=['POST'])
def post_assignment():
    # try:
    tutee_input = request.json.get('tutee_input',None)
    print(tutee_input)

    TuteeID = int(request.json.get('TuteeID'))
    AssignmentDayTime = tutee_input['AssignmentDayTime']
    Subject = tutee_input['Subject']
    Rate = float(tutee_input['Rate'])

    assignment = Assignment(TuteeID=TuteeID,AssignmentDayTime=AssignmentDayTime,
        Subject=Subject,Rate=Rate, Status='Open')

    try:
        db.session.add(assignment)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while posting the assignment. " + str(e)
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": assignment.json(),
            "message": "Assignment with ID {} is successfully created.".format(assignment.AssignmentID)
        }
    ), 201
    
# USER SCENARIO 2: Tutor to get all open assignments 
@app.route("/assignment")
def get_all_open_assignments():
    # assignmentlist = Assignment.query.all()
    assignmentlist = Assignment.query.filter_by(Status='Open').all()
    if len(assignmentlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "assignments": [assignment.json() for assignment in assignmentlist]
                },
                "message": "All open assignments are successfully returned."
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no open assignments."
        }
    ), 404

#Get an assignment by AssignmentID
@app.route("/assignment/<int:AssignmentID>")
def find_by_assignment_id(AssignmentID):
    assignment = Assignment.query.filter_by(AssignmentID=AssignmentID).first()
    if assignment:
        return jsonify(
            {
                "code": 200,
                "data": assignment.json(),
                "message": "Assignment with ID {} is successfully returned.".format(AssignmentID)
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "AssignmentID": AssignmentID
            },
            "message": "Assignment with ID {} is not found.".format(AssignmentID)
        }
    ), 404

#USER SCENARIO 3 Tutee post assignments and 
#USER SCENARIO 4.2 Tutee rejects/accepts tutor
@app.route("/assignment/<int:AssignmentID>", methods=['PUT'])
def update_assignment_status(AssignmentID):
    try:
        assignment = Assignment.query.filter_by(AssignmentID=AssignmentID).first()
        if not assignment:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "AssignmentID": AssignmentID
                    },
                    "message": "Assignment with ID {} is not found.".format(AssignmentID)
                }
            ), 404

        data = request.get_json()
        print(data)
        #Tutee post assignment and tutor applies, update assignment status from open to pending
        if assignment.Status=="Open" and data['Status']=="Pending":
            assignment.TutorID=data['TutorID']
            assignment.Status = data['Status']
        #Tutee rejects tutor's tuition assignment application, update assignment status from pending to open
        # and remove current tutor's ID
        elif assignment.Status=="Pending" and data['Status']=="Rejected":
            assignment.TutorID=None
            assignment.Status = 'Open'
        #Tutee accepts tutor's tuition assignment application, update assignment status from pending to accepted
        elif assignment.Status=="Pending" and data['Status']=="Accepted":
            assignment.Status = data['Status']
        else:
            return  jsonify(
                {
                    "code": 400,
                    "message": "An error occurred while updating the assignment." 
                }
            ), 400    
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": assignment.json(),
                "message": "Assignment with ID {} is successfully updated with new status.".format(AssignmentID)

            }
        ), 200
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "AssignmentID": AssignmentID
                },
                "message": "An error occurred while updating the assignment" + str(e)
            }
        ), 500

#USER SCENARIO 4.2 Tutee rejects/accepts tutor
#Filter by TuteeID
@app.route("/assignment/all/<int:TuteeID>")
def allPosts(TuteeID):
    assignmentlist = Assignment.query.filter_by(TuteeID=TuteeID).all()
    
    # for a in assignmentlist:
    #     print('im in the loop')
    #     print("assignments" )
    #     print(a)

    if len(assignmentlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "assignments": [assignment.json() for assignment in assignmentlist]
                },
                "message": "All assignments are successfully returned."
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no posted assignments."
        }
    ), 404

# USER SCENARIO 5 - Filter by TutorID and Status = 'Accepted'
@app.route("/assignment/accepted/<int:TutorID>")
def acceptedApplication(TutorID):
    filterlist = Assignment.query.filter_by(TutorID=TutorID).all()
    assignmentlist = []

    for a in filterlist:
        #print("im in the for loop!!")
        assignmentStatus = a.Status
        if (assignmentStatus == "Accepted"):
            assignmentlist.append(a)

    # print("assignments in list:" assignmentlist)
    if len(filterlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "assignments": [assignment.json() for assignment in assignmentlist]
                },
                "message": "All accepted assignments are successfully returned."
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no accepted assignments."
        }
    ), 404

###########################################################################################################################
#(OPTIONAL,ONLY FOR EASY CHECKING(FOR THE TEAM)
@app.route("/assignment/<string:Status>")
def get_assignment_by_status(Status):
    assignmentlist = Assignment.query.filter_by(Status=Status).all()
    if len(assignmentlist):
       
        return jsonify(
            {
                "code": 200,
                "data": {
                    "assignments": [assignment.json() for assignment in assignmentlist]
                },
                "message": "All assignments with status {} are successfully returned.".format(Status)
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no assignments with status {} .".format(Status)
        }
    ), 404

#Tutee delete posted assignment(allowed only when Status is still Open
#meaning no tutor has applied for it yet)
@app.route("/assignment/<int:AssignmentID>", methods=['DELETE'])
def delete_open_assignment(AssignmentID):
    assignment = Assignment.query.filter_by(AssignmentID=AssignmentID).first()
    if assignment.Status=="Open":
        db.session.delete(assignment)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "AssignmentID": AssignmentID
                },
                "message": "Assignment with ID {} is successfully deleted.".format(AssignmentID)
            }
        )
    else:
        return  jsonify(
            {
                "code": 400,
                "message": "An error occurred while deleting the assignment. The chosen assignment is still open" 
            }
        ), 400 

###########################################################################################################################
if __name__ == "__main__":
    print("This is flask for " + os.path.basename(__file__) + ": manage assignments ...")
    app.run(host="0.0.0.0", port=5001, debug=True)
