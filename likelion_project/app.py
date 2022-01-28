from flask import Flask, render_template, jsonify, request, session

app = Flask(__name__)

from pymongo import MongoClient  
import time 

client = MongoClient('localhost', 27017)  
db = client.likelion 

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/makeacc')
def makeacc():
    return render_template('create.html')

@app.route('/privatemedicalid')
def privatemedicalid():
    return render_template('privatemedicalid.html')

@app.route('/healthcare')
def healthcare():
    return render_template('findhealthcare.html')

@app.route('/medicalid')
def medicalid():
    return render_template('medicalid.html')

@app.route('/vaccine')
def vaccine():
    return render_template('vaccine.html')

@app.route('/afterlogin')
def afterlogin():
    return render_template('afterlogin.html')

app.secret_key = 'BAD_SECRET_KEY'

@app.route('/login', methods=['POST'])
def login():
    email_receive = request.form['email_give']
    password_receive = request.form['password_give']
    result = db.create.find_one({'personalemail':email_receive})
    session['email'] = email_receive
    if password_receive == result['password']:
        return jsonify({'result':'success'})
    else:
        return jsonify({'result':'bad'})

@app.route('/findzipcode', methods=['POST'])
def findzipcode():
    zipcode_receive = int(request.form['zipcode_give'])
    data = db.zipcodess.find_one({'ZIP': zipcode_receive}, {'_id':0})
    if data is None:
        data = db.zipcodess.find_one({'ZIP': str(zipcode_receive)}, {'_id': 0})
    zipcode_found = data['ZIP']
    if zipcode_found == zipcode_receive:
        results = list(db.zipcodess.find({'ZIP' :zipcode_receive}, {'_id':0}))
        return jsonify({'result':'success', 'msg':'Information loaded successfully','findzipcode':results})
    else:
        return jsonify({'result':'bad'})
    

@app.route('/findzipcode', methods=['GET'])
def show_zipcode():
    findzipcode = list(db.zipcodess.find({},{'_id':0}))
    return jsonify({'result':'success', 'findzipcode': findzipcode})

@app.route('/create', methods=['POST'])
def create():
    firstname_receive = request.form['firstname_give']
    lastname_receive = request.form['lastname_give']
    personalemail_receive = request.form['personalemail_give']
    password_receive = request.form['password_give']
    creates = {
        'firstname': firstname_receive,
        'lastname': lastname_receive,
        'personalemail': personalemail_receive,
        'password': password_receive
    }
    if db.create.find_one({'personalemail': personalemail_receive}) == None:
        db.create.insert_one(creates)
        return jsonify({'result':'success', 'msg': 'Account created successfully'})
    else:
        return jsonify({'result': 'fail'})

@app.route('/makemedicalid', methods=['POST'])
def makemedicalid():
    name_receive = request.form['name_give']
    address_receive = request.form['address_give']
    city_receive = request.form['city_give']
    zipcode_receive = request.form['zipcode_give']
    dateofbirth_receive = request.form['dateofbirth_give']
    date_receive = request.form['date_give']
    year_receive = request.form['year_give']
    bloodtype_receive = request.form['bloodtype_give']
    allergies_receive = request.form['allergies_give']
    weight_receive = request.form['weight_give']
    height_receive = request.form['height_give']
    emergencycontact_receive = request.form['emergencycontact_give']
    insurancecompany_receive = request.form['insurancecompany_give']
    insurancenumber_receive = request.form['insurancenumber_give']
    recentsymptoms_receive = request.form['recentsymptoms_give']
    idinfo = {
        'user': session['email'],
        'name': name_receive,
        'address': address_receive,
        'city': city_receive,
        'zipcode': zipcode_receive,
        'dateofbirth': dateofbirth_receive,
        'date': date_receive,
        'year': year_receive,
        'bloodtype': bloodtype_receive,
        'allergies': allergies_receive,
        'weight': weight_receive,
        'height': height_receive,
        'emergencycontact': emergencycontact_receive,
        'insurancecompany': insurancecompany_receive,
        'insurancenumber': insurancenumber_receive,
        'recentsymptoms': recentsymptoms_receive
    }
    db.makemedicalid.insert_one(idinfo)
    return jsonify({'result':'success', 'msg': 'Medical ID updated successfully'})

@app.route('/makemedicalid', methods=['GET'])
def show_medicalid():
    makemedicalid = list(db.makemedicalid.find({'user': session['email']},{'_id':0}))
    return jsonify({'result':'success', 'makemedicalid': makemedicalid})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)