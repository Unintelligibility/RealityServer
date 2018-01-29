from flask_restful import Resource
from pymongo import MongoClient
from bson.json_util import loads, dumps
from pprint import pprint
import json


class News(Resource):
    def __init__(self):
        client = MongoClient('mongodb://118.89.178.181/')
        db = client.reality
        self.news = db.news

    def get(self):
        res = {i: x for i, x in enumerate(self.news.find())}
        # pprint(res)
        res = json.loads(dumps(res))
        for x, y in res.items():
            y['_id'] = y['_id']['$oid']
        return res

    def post(self):
        pass
