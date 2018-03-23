from flask_restful import Resource
from RealityServer import mongo, app, auth
from passlib.apps import custom_app_context as pwd_context
from bson import ObjectId
from flask import request, abort, g
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from RealityServer.common import util


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
        return {'resultCode': 1, 'data': {'userid': str(userid), 'username': username, 'password': password}}, 201


class SignIn(Resource):
    def post(self):
        username = request.get_json(force=True)['username']
        password = request.get_json(force=True)['password']
        if verify_password(username, password):
            token = generate_auth_token()
            selected = False
            if mongo.db.profiles.find_one({'user_id': g.uid}):
                selected = True
            return {'resultCode': 1, 'data': {'_id': g.uid, 'token': token.decode('ascii'), 'selected': selected}}
        else:
            return util.data_fail('用户名密码错误'), 400


class Token(Resource):

    @auth.login_required
    def get(self):
        token = generate_auth_token()
        return {'token': token.decode('ascii'), 'duration': 3600, 'uid': g.uid}, 200


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = mongo.db.users.find_one({'username': username_or_token})
        if not user or not pwd_context.verify(password, user['password']):
            return False
    g.uid = str(user['_id'])
    return True


def generate_auth_token(expiration=600):
    s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({'_id': g.uid})


def verify_auth_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        print('expired')
        return None  # valid token, but expired
    except BadSignature:
        print('bad signature')
        return None  # invalid token
    users = mongo.db.users
    user = users.find_one({'_id': ObjectId(data['_id'])})
    return user


'''
推荐算法用户画像计算规则:
    用户选择兴趣,该标签+10
    用户阅读新闻，阅读超过6s +1 ,超过20s +2 ,收藏 +3 ,不感兴趣 -3       
'''


class Interest(Resource):
    # 用户选择兴趣权重为10
    interest_weight = 10

    @auth.login_required
    def post(self):
        likes = request.get_json(force=True)['likes']
        if not mongo.db.profiles.find_one({'user_id': g.uid}):
            mongo.db.profiles.insert_one({'user_id': g.uid, 'likes': {x: self.interest_weight for x in likes}})
        return util.post_success(), 200


class Profile(Resource):
    # 阅读超过6s +1 ,超过15s +2
    time_medium = 0
    weight_medium = 1
    time_long = 2
    weight_long = 2

    @auth.login_required
    def post(self):
        title = request.get_json()['title']
        source = request.get_json()['source']
        news_type = request.get_json()['news_type']
        news_tags = request.get_json()['news_tags'].split(';')
        if not news_type == '首页':
            news_tags.append(news_type)
        news_tags.append(source)
        reading_time = request.get_json()['reading_time']

        # if reading time is too short, ignore ( Another choice: analyse the title and the tags to update profile
        if reading_time < self.time_medium:
            return

        weight = 0
        if self.time_medium < reading_time < self.time_long:
            weight = self.weight_medium
        elif reading_time > self.time_long:
            weight = self.weight_long

        # insert into mongodb
        if mongo.db.profiles.find_one({'user_id': g.uid}):
            for tag in news_tags:
                mongo.db.profiles.update({'user_id': g.uid}, {'$inc': {'likes.' + tag: weight}})

        else:
            mongo.db.profiles.insert_one({'user_id': g.uid, 'likes': {tag: weight for tag in news_tags}})
        return util.post_success()
