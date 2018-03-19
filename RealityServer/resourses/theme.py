from flask_restful import Resource
from bson.json_util import loads, dumps
import json
from RealityServer import mongo
from RealityServer.common import util


class Theme(Resource):
    def __init__(self):
        self.theme_list = mongo.db.theme_list

    def get(self):
        res = {i: x for i, x in enumerate(self.theme_list.find())}
        res = json.loads(dumps(res))
        util.oid_transform(res)
        return {'resultCode': 1, 'data': res}


class Theme_News(Resource):
    def __init__(self):
        self.theme_news = mongo.db.theme_news

    def get(self, theme_name):
        res = {i: x for i, x in enumerate(self.theme_news.find({"theme": theme_name}))}
        res = json.loads(dumps(res))
        util.oid_transform(res)
        return {'resultCode': 1, 'data': res}
