from flask_restful import Resource
from bson.json_util import loads, dumps
from pprint import pprint
from RealityServer.common import util
import json
from RealityServer import mongo
from passlib.apps import custom_app_context as pwd_context
from flask import request, abort


class User:
    def __init__(self):
        self.users = mongo.db.users


class Register(Resource):
    def __init__(self):
        self.users = mongo.db.users

    def post(self):
        username = request.json.get('username')
        password = request.json.get('userpasswd')
        if not username or not password:
            abort(400)
        if self.users.find_one({'username': username}):
            return {'signupresult': 0, 'code': 400, 'message': '此用户名已被注册'}
        userid = self.users.insert_one(
            {'username': username,
             'password': pwd_context.encrypt(password)}
        )
        return {'signupresult': 1, 'code': 201, 'userid': str(userid), 'message': '注册成功！'}

# class SignIn(Resource):
#