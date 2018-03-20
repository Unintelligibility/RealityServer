from flask_restful import Resource
from bson.json_util import loads, dumps
import json
from RealityServer import mongo
from RealityServer.common import util

size=30

class Media(Resource):
    def __init__(self):
        self.media = mongo.db.star_media

    def get(self):
        res = {i: x for i, x in enumerate(self.media.find())}
        res = json.loads(dumps(res))
        util.oid_transform(res)
        return res

    def post(self):
        mongo.db.star_media.insert()

class Source(Resource):
    def __init__(self):
        self.source = mongo.db.source

    def get(self):
        res=self.source.find({}).sort("remark",-1).limit(size)
        res = json.loads(dumps(res))
        print(res)
        util.oid_transform_list(res)
        return res