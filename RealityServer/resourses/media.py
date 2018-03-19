from flask_restful import Resource
from bson.json_util import loads, dumps
import json
from RealityServer import mongo
from RealityServer.common import util


class Media(Resource):
    def __init__(self):
        self.media = mongo.db.star_media

    def get(self):
        # user_id
        res = {i: x for i, x in enumerate(self.media.find())}
        # pprint(res)
        res = json.loads(dumps(res))
        util.oid_transform(res)
        return res

    def post(self):
        # user_id
        mongo.db.star_media.insert()