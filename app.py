import json
from datetime import date, datetime
from random import random

from bson.json_util import dumps

import flask
from flask import request, jsonify
from pymongo import MongoClient

from dbconfig import app

client = MongoClient("mongodb://127.0.0.1:27017")  # host uri
db = client.cardservice  # Select the database

cardcomplaint = db.cardcomplaint
cardapply = db.cardapply
cardgeneration = db.cardgeneration
pingenerate = db.pingenerate

#complaint register process
@app.route('/complaintregister', methods=['POST'])
def complaintRegister():
    try:
        accno = request.json['accno']
        debitcardnumber = request.json['debitcardnumber']
        typeofaction = request.json['typeofaction']
        typeofblock = request.json['typeofblock']
        reasonforblocking = request.json['reasonforblocking']

        if accno and debitcardnumber and typeofaction and typeofblock and reasonforblocking and request.method == 'POST':
            ans = cardcomplaint.insert_one({'accno': accno, 'debitcardnumber': debitcardnumber, 'typeofaction': typeofaction,'typeofblock': typeofblock, 'reasonforblocking': reasonforblocking, 'createddate': getdate(),
                 'creationtime': gettime()})
            resp = jsonify("complaint registered successfully")
            resp.status_code = 200
            print(ans)
            return resp

    except Exception as e:
        return str(e)


def getdate():
    today = date.today()
    d = today.strftime("%d/%m/%y")
    return d


def gettime():
    now = datetime.now()
    t = now.strftime("%H:%M:%S")
    return t


@app.route('/updatecardstatus/<accno>', methods=['PUT'])
def updateCardStatus(accno):
    try:
        newaction = request.json['newaction']
        print(newaction)
        print(accno)
        print(type(accno))
        accountno=int(accno)
        findaction = cardcomplaint.find_one({'accno': accountno})
        typeofblock = findaction['typeofblock']
        if newaction == 'unblock':

            if typeofblock == 'temporary':
                if newaction and request.method == 'PUT':
                    ans = cardcomplaint.update_one({'accno': accountno},
                                                   {'$set': {'typeofaction': newaction, 'updateddate': getdate(),
                                                             'updatedtime': gettime()}})
                    print(ans)
                # return ans
                note = jsonify({"message": "updated successfully"})
                return note
            else:
                return jsonify({"message": "card id blocked permanently"})

        else:
            ans = cardcomplaint.update_one({'accno': accountno},
                                           {'$set': {'typeofaction': newaction, 'updateddate': getdate(), 'updatedtime': gettime()}})
            print(ans)
            return ans

        # else:

    except Exception as e:
        return str(e)


# result = cardcomplaint.find_one({"accno":accno})

@app.route('/viewallcomplaint', methods=['GET'])
def viewAllComplaint():
    complaint = cardcomplaint.find({})
    print(complaint)
    resp = dumps(complaint)
    return jsonify({"Result": resp})


@app.route('/viewcomplaint/<accno>', methods=['GET'])
def viewComplaint(accno):
    accountno=int(accno)
    user = cardcomplaint.find_one({'accno': accountno})
    resp = dumps(user)
    print(resp)
    return resp


@app.route('/applynewcard', methods=['POST'])
def applyNewCard():
    try:
        firstname = request.json['firstname']
        lastname = request.json['lastname']
        dob = request.json['dob']
        mobileno = request.json['mobileno']
        currentlocation = request.json['currentlocation']
        email = request.json['email']
        typeofemployment =request.json['typeofemployment']
        relationship_with_bank =request.json['relationship_with_bank']

        if request.method == 'POST':
            cardapply.insert_one({'firstname': firstname, 'lastname': lastname, 'dob': dob, 'mobileno': mobileno,
                                  'currentlocation': currentlocation, 'email': email,
                                  'typeofemployment': typeofemployment,
                                  'relationship_with_bank': relationship_with_bank})
            resp = jsonify("card applied successfully")
            resp.status_code = 200
            return resp

    except Exception as e:
        return str(e)
@app.route('/viewallapplication', methods=['GET'])
def viewAllApplication():
    application = cardapply.find({})
    print(application)
    resp = dumps(application)
    return jsonify({"Result": resp})


@app.route('/cardgeneration', methods=['POST'])
def cardGeneration():
    try:
        firstname = request.json['firstname']
        findall= cardgeneration.find({})
        findname= findall(firstname)
        if firstname in findall:

          if firstname and request.method == 'POST':
              ans = cardcomplaint.insert_one({'firstname': firstname, 'cardnumber': getcardno(), 'validfrom': getvalidfrom(),'validto': getvalidto(), 'createddate': getdate(), 'createdtime': gettime(),'ccvno':getccv()})
              resp = jsonify("card generated susccessfully")
              resp.status_code = 200
              print(ans)
              return resp
        else:
            return "apply for a card"
    except Exception as e:
        return str(e)

def getcardno():
    s = ''
    for i in range(16):
        s = s + str(random.randint(0, 9))
        return s

def getvalidfrom():
    todays_date = date.today()
    cy=todays_date.year
    return cy



def getvalidto():
    todays_date = date.today()
    cy=todays_date.year + 4
    return  cy
def getccv():
    num= random.randint(100,999)
    return num

@app.route('/viewallcard', methods=['GET'])
def viewAllCard():
    card = cardgeneration.find({})
    print(card)
    resp = dumps(card)
    return jsonify({"Result": resp})


@app.route('/generatepin',methods=['POST'])
def generatePin():
    try:
      accno=request.json('accno')
      mobileno=request.json('mobileno')
      if request.method == 'POST':
        Ans = pingenerate.insert_one({'accno':accno,'cardno':getcardno(),'ccvno':getccv(),'mobileno':mobileno,'pin':getpin()})
        resp = jsonify("card applied successfully")
        resp.status_code = 200
        return resp
    except Exception as e:
        return str(e)
def getpin():
    pi=random.randint(1000,9999)
    return pi

if __name__ == "__main__":
    app.run(debug=True)
