"""
define app and routes
"""
from flask import Flask, Blueprint
from flask_restful import Resource, Api, url_for
from flask_pymongo import PyMongo
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__, instance_relative_config=True)

app.config.from_object('config')
app.config.from_pyfile('config.py')

mongo = PyMongo(app)
auth = HTTPBasicAuth()

from RealityServer.resourses.news import News,Recommend,Report
from RealityServer.resourses.media import Media
from RealityServer.resourses.user import Register, SignIn

api = Api(app)
api.add_resource(News, '/read')
api.add_resource(Report, '/<string:new_id>/report')
api.add_resource(Recommend, '/<string:new_id>/recommend')
api.add_resource(Media, '/staroffice')
api.add_resource(Register, '/signup')
api.add_resource(SignIn, '/signin')

if __name__ == '__main__':
    app.run()
