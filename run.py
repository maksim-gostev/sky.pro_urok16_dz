import json
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

import utils

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.url_map.strict_slashes = False
db = SQLAlchemy(app)


class Users(db.Model):
    __tablname__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    email = db.Column(db.Text(200))
    first_name = db.Column(db.Text(200))
    last_name = db.Column(db.Text(200))
    phone = db.Column(db.Text(200))
    role = db.Column(db.Text(200))


class Offers(db.Model):
    __tablename__ = "offers"

    id = db.Column(db.Integer, primary_key=True)
    executor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    executor = db.relationship('Users')
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    order = db.relationship('Orders')


class Orders(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.Text(200))
    description = db.Column(db.Text(200))
    end_date = db.Column(db.Text(200))
    name = db.Column(db.Text(200))
    price = db.Column(db.Integer)
    start_date = db.Column(db.Text(200))
    executor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    executor = db.relationship('Users')
    customer_id = db.Column(db.Integer)


db.create_all()

with open('users.json', 'r', encoding='utf-8') as file:
    json_users: [list] = json.load(file)

for json_user in json_users:
    user_ = Users(
        id=json_user['id'],
        age=json_user['age'],
        email=json_user['email'],
        first_name=json_user['first_name'],
        last_name=json_user['last_name'],
        phone=json_user['phone'],
        role=json_user['role'])
    db.session.add(user_)

with open('offers.json', 'r', encoding='utf-8') as file:
    json_offers: [list] = json.load(file)

for json_offer in json_offers:
    offer_ = Offers(
        executor_id=json_offer['executor_id'],
        id=json_offer['id'],
        order_id=json_offer['order_id'])

    db.session.add(offer_)

with open('orders.json', 'r', encoding='utf-8') as file:
    json_orders: [list] = json.load(file)

for json_order in json_orders:
    order_= Orders(
        address=json_order['address'],
        customer_id=json_order['customer_id'],
        description=json_order['description'],
        end_date=json_order['end_date'],
        executor_id=json_order['executor_id'],
        id=json_order['id'],
        name=json_order['name'],
        price=json_order['price'],
        start_date=json_order['start_date'])

    db.session.add(order_)
db.session.commit()


@app.get('/users')
def get_all_users():
    result = []
    users = Users.query.all()
    for user in users:
        result.append(utils.instance_to_dict_users(user))
    return jsonify(result)


@app.get('/users/<int:uid>')
def get_one_user(uid):
    user = Users.query.get(uid)
    return jsonify(utils.instance_to_dict_users(user))


@app.get('/orders')
def get_all_orders():
    result = []
    orders = Orders.query.all()
    for order in orders:
        result.append(utils.instance_to_dict_orders(order))
    return jsonify(result)


@app.get('/orders/<int:orid>')
def get_one_orders(orid):
    order = Orders.query.get(orid)
    return jsonify(utils.instance_to_dict_orders(order))


@app.get('/offers')
def get_all_offers():
    result = []
    offers = Offers.query.all()
    for offer in offers:
        result.append(utils.instance_to_dict_offers(offer))
    return jsonify(result)


@app.get('/offers/<int:ofid>')
def get_one_offers(ofid):
    offer = Offers.query.get(ofid)
    return jsonify(utils.instance_to_dict_offers(offer))


@app.post('/users')
def post_user():
    data = request.json
    user = Users(
        age=data.get('age'),
        email=data.get('email'),
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        phone=data.get('phone'),
        role=data.get('role')
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(utils.instance_to_dict_users(user))


@app.put('/users/<int:uid>')
def put_user(uid):
    data = request.json
    user = Users.query.get(uid)

    user.age = data['age'],
    user.email = data['email'],
    user.first_name = data['first_name'],
    user.last_name = data['last_name'],
    user.phone = data['phone'],
    user.role = data['role']

    db.session.add(user)
    db.session.commit()


@app.route('/users/<int:uid>/delete')
def delete_users(uid):
    user = Users.query.get(uid)
    db.session.delete(user)
    db.session.commit()
    return jsonify("")


@app.post('/orders')
def post_orders():
    data = request.json
    order = Orders(
        address=data.get('address'),
        customer_id=data.get('customer_id'),
        description=data.get('description'),
        end_date=data.get('end_date'),
        executor_id=data.get('executor_id'),
        name=data.get('name'),
        price=data.get('price'),
        start_date=data.get('start_date')
    )
    db.session.add(order)
    db.session.commit()
    return jsonify(utils.instance_to_dict_orders(order))


@app.put('/orders/<int:orid>')
def put_orders(orid):
    data = request.json
    order = Users.query.get(orid)

    order.age = data['age'],
    order.email = data['email'],
    order.first_name = data['first_name'],
    order.last_name = data['last_name'],
    order.phone = data['phone'],
    order.role = data['role']

    db.session.add(order)
    db.session.commit()


@app.route('/orders/<int:orid>/delete')
def delete_orders(orid):
    order = Users.query.get(orid)
    db.session.delete(order)
    db.session.commit()
    return jsonify("")


@app.post('/offers')
def post_offers():
    data = request.json
    offer = Offers(
        executor_id=data.get('executor_id'),
        id=data.get('id'),
        order_id=data.get('order_id')
    )
    db.session.add(offer)
    db.session.commit()
    return jsonify(utils.instance_to_dict_offers(offer))


@app.put('/offers/<int:ofid>')
def put_offers(ofid):
    data = request.json
    offer = Users.query.get(ofid)

    offer.age = data['age'],
    offer.email = data['email'],
    offer.first_name = data['first_name'],
    offer.last_name = data['last_name'],
    offer.phone = data['phone'],
    offer.role = data['role']

    db.session.add(offer)
    db.session.commit()


@app.route('/offers/<int:ofid>/delete')
def delete_offers(ofid):
    offer = Users.query.get(ofid)
    db.session.delete(offer)
    db.session.commit()
    return jsonify("")


if __name__ == "__main__":
    app.run()
