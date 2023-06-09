from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient  

client = MongoClient('localhost', 27017)  
db = client.likelion 

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/orders', methods=['POST'])
def do_order():
    name_receive = request.form['name_give']
    amount_receive = request.form['amount_give']
    address_receive = request.form['address_give']
    number_receive = request.form['number_give']
        
    order = {
        'name': name_receive,
        'amount': amount_receive,
        'address': address_receive,
        'number': number_receive
    }

    db.orders.insert_one(order)
    return jsonify({'result': 'success', 'msg': '주문완료!'})

@app.route('/orders', methods=['GET'])
def show_order():
    orders = list(db.orders.find({},{'_id':0}))
    return jsonify({'result':'success', 'orders': orders})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)