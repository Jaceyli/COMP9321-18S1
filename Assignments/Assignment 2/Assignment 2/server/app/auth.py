from functools import wraps
from flask import request,jsonify
from flask_restful import abort
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer)
SECRET_KEY = "COMP9321"

def authenticate_admin_by_token(token):
    if not token:
       return False
    s = Serializer(SECRET_KEY)
    username = s.loads(token.encode())
    if username == 'admin':
      return True
    return False

def authenticate_by_token(token):
    if not token:
       return False
    s = Serializer(SECRET_KEY)
    username = s.loads(token.encode())
    if username in ['admin','guest']:
      return True
    return False

def admin_required(f, message="You are not admin authorized"):
    @wraps(f)
    def decorated_function(*args, **kwargs):
       token = request.headers.get("AUTH_TOKEN")
       if authenticate_admin_by_token(token):
           return f(*args, **kwargs)
       return jsonify(message=message), 401, {'Access-Control-Allow-Origin': '*'}
    return decorated_function

def login_required(f, message="You are not login authorized"):
    @wraps(f)
    def decorated_function(*args, **kwargs):
       token = request.headers.get("AUTH_TOKEN")
       if authenticate_by_token(token):
           return f(*args, **kwargs)
       return jsonify(message=message), 401, {'Access-Control-Allow-Origin': '*'}
    return decorated_function


