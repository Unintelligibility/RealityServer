from flask_restful import Resource
from bson.json_util import loads, dumps
from pprint import pprint
from RealityServer.common import util
import json
from RealityServer import mongo, app, auth
from passlib.apps import custom_app_context as pwd_context
from flask import request, abort, g
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


class Register(Resource):
    def __init__(self):
        self.users = mongo.db.users

    def post(self):
        get = request.get_json(force=True)
        username = get['username']
        password = get['password']
        if 'icon' in get.keys():
            icon = request.get_json(force=True)['icon']
        else:
            icon = ''
        if not username or not password:
            return {'resultCode': 0, 'resultMessage': 'username and password cannot be none'}, 400
        if self.users.find_one({'username': username}):
            return {'resultCode': 0, 'resultMessage': 'username has been taken'}, 400
        userid = self.users.insert_one(
            {'username': username,
             'password': pwd_context.encrypt(password),
             'icon': icon}
        ).inserted_id
        return {'resultCode': 1, 'data': {'userid': str(userid)}}, 201


class SignIn(Resource):
    def post(self):
        username = request.get_json(force=True)['username']
        password = request.get_json(force=True)['password']
        if verify_password(username, password):
            token = generate_auth_token()
            return {'resultCode': 1, 'data': {'_id': str(g.uid), 'token': token.decode('ascii')}}
        else:
            return {'resultCode': 0}, 400


def generate_auth_token(expiration=600):
    s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({'_id': g.uid})


def verify_auth_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None  # valid token, but expired
    except BadSignature:
        return None  # invalid token
    users = mongo.db.users
    user = users.find_one({'_id': data['_id']})
    return user


@app.route('/token')
@auth.login_required
def get_auth_token():
    token = generate_auth_token()
    return {'token': token.decode('ascii'), 'duration': 3600}


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = mongo.db.users.find_one({'username': username_or_token})
        if not user or not pwd_context.verify(password, user['password']):
            return False
    g.uid = user['_id']
    return True
