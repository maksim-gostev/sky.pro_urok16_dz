import json
from flask import Flask, jsonify
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
    order_id = db.Column(db.Integer)


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
    customer_id = db.Column(db.Integer, db.ForeignKey('offers.id'))


db.create_all()

with open('users.json', 'r', encoding='utf-8') as file:
    json_users: [list] = json.load(file)

for json_user in json_users:
    user = Users(
        id=json_user['id'],
        age=json_user['age'],
        email=json_user['email'],
        first_name=json_user['first_name'],
        last_name=json_user['last_name'],
        phone=json_user['phone'],
        role=json_user['role'])
    db.session.add(user)

with open('offers.json', 'r', encoding='utf-8') as file:
    json_offers: [list] = json.load(file)

for json_offer in json_offers:
    offer = Offers(
    executor_id=json_offer['executor_id'],
    id=json_offer['id'],
    order_id=json_offer['order_id'])

    db.session.add(offer)

with open('orders.json', 'r', encoding='utf-8') as file:
    json_orders: [list] = json.load(file)

for json_order in json_orders:
    order = Orders(
        address=json_order['address'],
        customer_id=json_order['customer_id'],
        description=json_order['description'],
        end_date=json_order['end_date'],
        executor_id=json_order['executor_id'],
        id=json_order['id'],
        name=json_order['name'],
        price=json_order['price'],
        start_date=json_order['start_date'])

    db.session.add(order)
db.session.commit()



@app.route('/users')
def get_all_users():
    result = []
    users = Users.query.all()
    for user in users:
        result.append(utils.instance_to_dict_users(user))
    return jsonify(result)


@app.route('/users/<int:uid>')
def get_one_user(uid):
    user = Users.query.get(uid)
    return jsonify(utils.instance_to_dict_users(user))


if __name__ == "__main__":
    app.run()
