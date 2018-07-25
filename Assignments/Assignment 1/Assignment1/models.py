# Order : type of coffee, cost, additions (e.g., skim milk, extra shot)
# Payment : payment type (cash or card), payment amount, card details (if card)
import time


class Order:
    def __init__(self, order_id, coffee_type, cost, status, payment, additions=None):
        self.order_id = order_id
        self.coffee_type = coffee_type
        self.cost = cost
        self.additions = additions
        self.status = status
        self.payment = payment


class Payment:
    def __init__(self, order_id, pay_type, amount, pay_time, card_info=None):
        self.order_id = order_id
        self.pay_type = pay_type
        self.amount = amount
        self.card_info = card_info
        self.pay_time = pay_time
