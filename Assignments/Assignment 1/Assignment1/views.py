import time
from flask import Flask
from flask import jsonify
from flask_restful import reqparse
from models import Order, Payment

app = Flask(__name__)
coffee = {"Latte": 3.5, "Cappuccino": 4, "Macchiato": 3, "Espresso": 3.5, "Mocha": 4}
orders = []
payments = []


@app.route("/Order", methods=['POST'])
def create_order():
    parser = reqparse.RequestParser()
    # parser.add_argument('id', type=str)
    parser.add_argument('coffee_type', type=str)
    parser.add_argument('additions', type=str)
    args = parser.parse_args()

    # order_id = args.get("id")
    coffee_type = args.get("coffee_type")
    additions = None
    if args.get("additions") is not None:
        additions = [i for i in args.get("additions").split(',')]
    id = str(int(time.time()))
    if coffee_type in coffee.keys():
        cost = coffee[coffee_type]
        status = "Placed"
        payment = "F"
        if additions:
            orders.append(Order(id, coffee_type, cost, status, payment, additions=additions))
        else:
            orders.append(Order(id, coffee_type, cost, status, payment))
        return jsonify(order_id=id, coffee_type=coffee_type, cost=cost, payment='/payOrder/'+id), 201
    return jsonify(coffee_type=False), 404


@app.route("/Order/<id>", methods=['GET'])
def get_order(id):
    for order in orders:
        if order.order_id == id:
            if order.payment != 'F':
                return jsonify(order_id=order.order_id, coffee_type=order.coffee_type, additions=order.additions,payment=order.payment), 200
            else:
                return jsonify(order_id=order.order_id, coffee_type=order.coffee_type, additions=order.additions, payment='/payOrder/'+order.order_id), 200
    return jsonify(order_id=False), 404


@app.route("/Order/<id>", methods=['PUT'])
def update_order(id):
    parser = reqparse.RequestParser()
    parser.add_argument('coffee_type', type=str)
    parser.add_argument('additions', type=str)
    args = parser.parse_args()

    coffee_type = args.get("coffee_type")
    additions = None
    if args.get("additions"):
        additions = [i for i in args.get("additions").split(',')]

    for order in orders:
        if order.order_id == id:
            if coffee_type is None:
                if order.payment == 'F' and order.status == 'Placed':
                    return jsonify(success="You can change your order."), 100
                else:
                    return jsonify(error="The order can not be changed."), 417
            if order.payment == 'F' and order.status == 'Placed':
                    if coffee_type in coffee:
                        cost = coffee[coffee_type]
                        orders.remove(order)
                        orders.append(Order(id, coffee_type, cost, "Placed", "F", additions=additions))
                        return jsonify(order_id=id, coffee_type=coffee_type, cost=cost, additions=additions), 200
                    else:
                        return jsonify(coffee_type=False), 404
            else:
                return jsonify(error="The order can not be changed."), 409
    return jsonify(order_id=False), 404


@app.route("/Order/<id>", methods=['PATCH'])
def update_status(id):
    parser = reqparse.RequestParser()
    parser.add_argument('status', type=str)
    args = parser.parse_args()
    status = args.get("status")
    if status not in ['Progressing', 'Cancelled']:
        return jsonify(error="Wrong status!"), 400

    for order in orders:
        if order.order_id == id:
            if order.status == 'Cancelled':
                return jsonify(error='The order has been cancelled.'), 409
            if order.status == 'Progressing' and status == 'Progressing':
                return jsonify(error='The order has been progressing.'), 409
            if order.status == 'Placed' and status == 'Progressing':
                order.status = status
                return jsonify(order_id=order.order_id, status=status), 200
            if status == 'Cancelled':
                if order.payment != 'F':
                    return jsonify(error="The order can not be cancelled after payment!"), 409
                else:
                    order.status = status
                    return jsonify(order_id=order.order_id, status=status), 200

    return jsonify(order_id=False), 404


@app.route("/Order/<id>", methods=['DELETE', 'POST'])
def delete_order(id):
    for order in orders:
        if order.order_id == id:
            if order.payment != 'F':
                if order.status == 'Progressing':
                    orders.remove(order)
                    return jsonify(order_id=id), 200
                else:
                    return jsonify(error='The coffee has not made yet.'), 400
            else:
                return jsonify(error='The coffee has not paid yet.'), 400
    return jsonify(order_id=False), 404


@app.route("/Orders", methods=['GET'])
def get_orders():
    response = jsonify(resultSize=orders.__len__(), result=[order.__dict__ for order in orders]), 200
    return response


@app.route("/OpenOrders", methods=['GET'])
def get_open_orders():
    open_orders = []
    for order in orders:
        if order.status != 'Cancelled':
            open_orders.append(order)
    response = jsonify(resultSize=orders.__len__(), result=[order.__dict__ for order in open_orders]), 200
    return response


@app.route("/Payment/<id>", methods=['PUT'])
def pay_order(id):
    parser = reqparse.RequestParser()
    parser.add_argument('pay_type', type=str)
    parser.add_argument('amount', type=float)
    parser.add_argument('card_info', type=str)
    args = parser.parse_args()

    pay_type = args.get("pay_type")
    amount = args.get("amount")
    card_info = None

    if pay_type not in ['card', 'cash']:
        return jsonify(error='Wrong payment type. (card or cash)'), 400
    if pay_type == 'card':
        card_info = args.get("card_info")
    # print(pay_type, amount, card_info)
    for order in orders:
        if order.order_id == id:
            if order.status == "Cancelled":
                return jsonify(error="You order has been cancelled."), 409
            for p in payments:
                if p.order_id == id:
                    return jsonify(error="You already paid for your coffee."), 409
            else:
                if amount == order.cost:
                    pay_time = time.ctime()
                    payments.append(Payment(id, pay_type, amount, pay_time, card_info))
                    if pay_type == 'card':
                        order.payment = {"pay_time": pay_time, "pay_type": pay_type, "card_info":card_info}
                        return jsonify(order_id=id, pay_type=pay_type, amount=amount, pay_time=pay_time, card_info=card_info), 201
                    else:
                        order.payment = {"pay_time": pay_time, "pay_type": pay_type}
                        return jsonify(order_id=id, pay_type=pay_type, amount=amount, pay_time=pay_time), 201
                else:
                    return jsonify(error="Sorry. The cost is not correct."), 400
    return jsonify(order_id=False), 404


@app.route("/Payment/<id>", methods=['GET'])
def get_order_payment_info(id):
    for p in payments:
        if p.order_id == id:
            return jsonify(p.__dict__), 200
    return jsonify(error="The order "+id+" has not paid yet."), 404


