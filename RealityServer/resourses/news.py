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
        res = {i: x for i, x in enumerate(self.news.find().limit(20))}  # TODO: add recommend method and newest news
        # pprint(res)
        res = json.loads(dumps(res))
        util.oid_transform(res)
        return res

    def post(self):
        pass


class Recommend(Resource):
    def __init__(self):
        pass
