
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
#  or 'mysql+mysqlconnector://root@localhost:3306/tutor'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)
CORS(app)


class Tutor(db.Model):
    __tablename__ = 'Tutor'

    TutorID = db.Column(db.Integer, primary_key=True)
    TutorName = db.Column(db.String(32), nullable=False)
    TutorGender = db.Column(db.String(1), nullable=False)
    TutorPhone = db.Column(db.Integer, nullable=False)
    TutorAge = db.Column(db.Integer, nullable=False)
    TutorQualification = db.Column(db.String(300), nullable=False)
    TutorTelegramID = db.Column(db.String(32), nullable=False)
    TutorTeleChatID=db.Column(db.Integer, nullable=False)
    TutorEmail=db.Column(db.Text, nullable=False)

    def json(self):
        dto = {
            'TutorID': self.TutorID,
            'TutorName': self.TutorName,
            'TutorGender': self.TutorGender,
            'TutorPhone': self.TutorPhone,
            'TutorAge': self.TutorAge,
            'TutorQualification': self.TutorQualification,
            'TutorTelegramID': self.TutorTelegramID,
            'TutorTeleChatID':self.TutorTeleChatID,
            'TutorEmail':self.TutorEmail
        }
        return dto

    #     dto['tutor_item'] = []
    #     for oi in self.order_item:
    #         dto['tutor_item'].append(oi.json())

    #     return dto

@app.route("/tutor")
def get_all():
    tutorlist = Tutor.query.all()
    if len(tutorlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "tutors": [tutor.json() for tutor in tutorlist]
                },
                "message": "All existing tutors are successfully returned."
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no tutors."
        }
    ), 404


@app.route("/tutor/<int:TutorID>")
def find_by_tutor_id(TutorID):
    tutor = Tutor.query.filter_by(TutorID=TutorID).first()
    if tutor:
        return jsonify(
            {
                "code": 200,
                "data": tutor.json(),
                "message": "Tutor with id {} is successfully returned.".format(TutorID)
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "TutorID": TutorID
            },
            "message": "Tutor not found."
        }
    ), 404

###########################################################################################################################
@app.route("/tutor", methods=['POST'])
def create_tutor():
    TutorTeleChatID = request.json.get('TutorTeleChatID')
    if (Tutor.query.filter_by(TutorTeleChatID=TutorTeleChatID).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "TutorTeleChatID": TutorTeleChatID
                },
                "message": "Tutor already exists."
            }
        ), 400

    TutorID = request.json.get('TutorID', None)
    TutorName = request.json.get('TutorName')
    TutorGender = request.json.get('TutorGender')
    TutorPhone = int(request.json.get('TutorPhone'))
    TutorAge = int(request.json.get('TutorAge'))
    TutorQualification = request.json.get('TutorQualification')
    TutorTelegramID = request.json.get('TutorTelegramID')
    TutorTeleChatID=int(request.json.get('TutorTeleChatID'))
    TutorEmail=request.json.get('TutorEmail')
    tutor = Tutor(TutorID=TutorID,TutorName=TutorName, TutorGender=TutorGender,
            TutorPhone=TutorPhone, TutorAge=TutorAge, TutorQualification=TutorQualification,
            TutorTelegramID=TutorTelegramID,TutorTeleChatID=TutorTeleChatID, TutorEmail=TutorEmail)

    try:
        db.session.add(tutor)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating new tutor account. " + str(e)
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": tutor.json(),
            "message": "Tutor with ID {} is successfully created.".format(tutor.TutorID)
        }
    ), 201


@app.route("/tutor/<int:TutorID>", methods=['PUT'])
def update_tutor(TutorID):
    # TutorID = request.json.get('TutorID', None)

    try:
        tutor = Tutor.query.filter_by(TutorID=TutorID).first()
        if not tutor:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "TutorID": TutorID
                    },
                    "message": "Tutor not found."
                }
            ), 404

        # update particulars
        data = request.get_json()
        if "TutorName" in data:
            tutor.TutorName = data['TutorName']
        if "TutorPhone" in data:
            tutor.TutorPhone = data['TutorPhone']
        if "TutorQualification" in data:
            tutor.TutorQualification = data['TutorQualification']
        if "TutorAge" in data:
            tutor.TutorAge = data['TutorAge']
        if "TutorTelegramID" in data:
            tutor.TutorTelegramID = data['TutorTelegramID']
        if "TutorEmail" in data:
            tutor.TutorEmail = data['TutorEmail']
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": tutor.json(),
                "message": "Tutor with ID {} is successfully updated with new details.".format(TutorID)
            }
        ), 200
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "TutorID": TutorID
                },
                "message": "An error occurred while updating the order. " + str(e)
            }
        ), 500
###########################################################################################################################

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage tutor ...")
    app.run(host='0.0.0.0',port=5002, debug=True)
