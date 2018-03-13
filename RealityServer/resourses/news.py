from flask import request
from flask_restful import Resource
from bson.json_util import loads, dumps
from RealityServer.common import util
import json
from RealityServer import mongo


class News(Resource):
    def __init__(self):
        self.news = mongo.db.news

    def get(self, user_id):
        limit_news = 15
        analyse_num = 30
        global start

        news_num = self.news.count()
        print(news_num)
        if start >= news_num:
            start = 0
        news = self.news.find()[start:start + analyse_num]
        start = start + analyse_num  # TODO: using redis to mantain the user pool

        profile = mongo.db.profiles.find_one({'user_id': user_id})
        if profile:
            likes = profile['likes']

            recommend_score = []
            # 初始版本-非向量化,低效率实现
            # TODO: 向量化实现，加入正则化与IDF (建立tag链表
            # TODO: use Spark to improve speed
            for new in news:
                source = new['source']
                news_type = new['news_type']
                news_tags = new['news_tags'].split(';')
                if not news_type == '首页':
                    news_tags.append(news_type)
                news_tags.append(source)

                recommend_score.append(sum([likes.get(tag, 0) for tag in news_tags]))

            news.rewind()
            res_sort = [(new, score) for new, score in zip(news, recommend_score)]
            res_sort.sort(key=lambda item: item[1], reverse=True)
            res = [new for new, _ in res_sort[:limit_news]]
        else:
            res = news[:limit_news]

        res = {i: x for i, x in
               enumerate(res)}
        res = json.loads(dumps(res))
        util.oid_transform(res)
        return util.data_success(res)


class Relate(Resource):
    """单条新闻类似阅读"""

    def __init__(self):
        self.news = mongo.db.news

    def get(self, new_id):
        res = [x for x in self.news.find().limit(3)]  # TODO: add recommend relative
        res = json.loads(dumps(res))
        util.oid_transform(res)
        return res


class Report(Resource):
    def post(self):
        mongo.db.report.insert_one(
            {'news_id': request.get_json()['news_id'], 'reason': request.get_json(force=True)['reason']})
        return {'resultCode': 1}


start = 0
