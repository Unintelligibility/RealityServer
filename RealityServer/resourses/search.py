from flask import request
from flask_restful import Resource
from RealityServer.common import util
from RealityServer import mongo
import re
from pickle import dumps

class Search(Resource):
	def __init__(self):
		self.news = mongo.db.news

	def get(self,keyword,start,size):
		if keyword is None or start is None or size is None :
			return {'resultCode': 0},400
		regx = re.compile("/"+keyword.encode()+"/", re.IGNORECASE)
		# print(keyword.encode("utf-8"))
		res={i: util.bytesToStr(news) for i,news in enumerate(self.news.find({"title":regx}).sort("time",-1).skip(start*10).limit(size))}
		util.oid_transform(res)
		return util.data_success(res)

	def post(self):
	    pass