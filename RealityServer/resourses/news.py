from flask import request
from flask_restful import Resource
from bson.json_util import loads, dumps
from pprint import pprint
from RealityServer.common import util
import json
from RealityServer import mongo

class News(Resource):
    def __init__(self):
        self.news = mongo.db.news

    def get(self):
        res = {i: util.bytesToStr(x) for i, x in enumerate(self.news.find().limit(20))}  # TODO: add recommend method and newest news
        pprint(res)
        res = json.loads(dumps(res))
        util.oid_transform(res)
        return util.data_success(res)
    
    def post(self):
        pass


class Recommend(Resource):
    def __init__(self):
        self.news = mongo.db.news

    def get(self, new_id):
        res = {i: x for i, x in enumerate(self.news.find().limit(3))}  # TODO: add recommend relative
        res = json.loads(dumps(res))
        util.oid_transform(res)
        return res


class Report(Resource):
    def post(self, new_id):
        mongo.db.report.insert_one({'new_id': new_id, 'reason': request.get_json(force=True)['reason']})
        return {'resultCode': 1}
