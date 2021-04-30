import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
#  or 'mysql+mysqlconnector://root@localhost:3306/tutee'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)
CORS(app)


class Tutee(db.Model):
    __tablename__ = 'Tutee'

    TuteeID = db.Column(db.Integer, primary_key=True)
    TuteeName = db.Column(db.String(32), nullable=False)
    TuteeGender = db.Column(db.String(1), nullable=False)
    TuteePhone = db.Column(db.Integer, nullable=False)
    TuteeGrade = db.Column(db.String(32), nullable=False)
    TuteeLocation = db.Column(db.String(32), nullable=False)
    TuteeTelegramID = db.Column(db.String(32), nullable=False)
    TuteeTeleChatID=db.Column(db.Integer, nullable=False)
    TuteeEmail=db.Column(db.Text, nullable=False)

    def json(self):
        dto = {
            'TuteeID': self.TuteeID ,
            'TuteeName': self.TuteeName,
            'TuteeGender': self.TuteeGender,
            'TuteePhone': self.TuteePhone,
            'TuteeGrade': self.TuteeGrade,
            'TuteeLocation': self.TuteeLocation,
            'TuteeTelegramID': self.TuteeTelegramID,
            'TuteeTeleChatID': self.TuteeTeleChatID,
            'TuteeEmail': self.TuteeEmail
        }
        return dto

@app.route("/tutee")
def get_all():
    tuteelist = Tutee.query.all()
    if len(tuteelist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "tutees": [tutee.json() for tutee in tuteelist]
                },
                 "message": "All existing tutees are successfully returned."
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no tutees."
        }
    ), 404


@app.route("/tutee/<int:TuteeID>")
def find_by_tutee_id(TuteeID):
    tutee = Tutee.query.filter_by(TuteeID=TuteeID).first()
    if tutee:
        return jsonify(
            {
                "code": 200,
                "data": tutee.json(),
                "message": "Tutee with id {} is successfully returned.".format(TuteeID)
            },
              
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "TuteeID": TuteeID
            },
            "message": "Tutee not found."
        }
    ), 404

###########################################################################################################################
@app.route("/tutee", methods=['POST'])
def create_tutee():
    TuteeName = request.json.get('TuteeName')
    TuteeGender = request.json.get('TuteeGender')
    TuteePhone = int(request.json.get('TuteePhone'))
    TuteeGrade = request.json.get('TuteeGrade')
    TuteeLocation = request.json.get('TuteeLocation')
    TuteeTelegramID = request.json.get('TuteeTelegramID')
    TuteeTeleChatID=int(request.json.get('TuteeTeleChatID'))
    TuteeEmail=request.json.get('TuteeEmail')
    tutee = Tutee(TuteeName=TuteeName, TuteeGender=TuteeGender,
            TuteePhone=TuteePhone, TuteeGrade=TuteeGrade, TuteeLocation=TuteeLocation,
            TuteeTelegramID=TuteeTelegramID,TuteeTeleChatID=TuteeTeleChatID,TuteeEmail=TuteeEmail)
    try:
        db.session.add(tutee)
        db.session.commit()
    
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating new tutee account. " + str(e)
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": tutee.json(),
            "message": "Tutee with ID {} is successfully created.".format(tutee.TuteeID)
        }
    ), 201


@app.route("/tutee/<int:TuteeID>", methods=['PUT'])
def update_tutee(TuteeID):
    try:
        tutee = Tutee.query.filter_by(TuteeID=TuteeID).first()
        if not tutee:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "TuteeID": TuteeID
                    },
                    "message": "Tutee not found."
                }
            ), 404

        # update particulars
        data = request.get_json()
        if "TuteeName" in data:
            tutee.TuteeName = data['TuteeName']
        if "TuteePhone" in data:
            tutee.TuteePhone = data['TuteePhone']
        if "TuteeGrade" in data:
            tutee.TuteeGrade = data['TuteeGrade']
        if "TuteeLocation" in data:
            tutee.TuteeLocation = data['TuteeLocation']
        if "TuteeTelegramID" in data:
            tutee.TuteeTelegramID = data['TuteeTelegramID']
        if "TuteeEmail" in data:
            tutee.TuteeEmail = data['TuteeEmail']
        
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": tutee.json(),
                "message": "Tutee with ID {} is successfully updated with new details.".format(TuteeID)
            }
        ), 200
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "TuteeID": TuteeID
                },
                "message": "An error occurred while updating the tutee's details. " + str(e)
            }
        ), 500
###########################################################################################################################

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage tutee ...")
    app.run(host='0.0.0.0',port=5000, debug=True)