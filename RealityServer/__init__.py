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

from RealityServer.resourses.news import News, Relate, Report
from RealityServer.resourses.media import Media,Source
from RealityServer.resourses.user import Register, SignIn, Interest, Token, Profile
from RealityServer.resourses.theme import Theme, Theme_News
from RealityServer.resourses.search import Search

api = Api(app)
api.add_resource(News, '/<string:user_id>/read')
api.add_resource(Relate, '/<string:new_id>/relate')
api.add_resource(Report, '/report')
api.add_resource(Media, '/staroffice')
api.add_resource(Register, '/signup')
api.add_resource(SignIn, '/signin')
api.add_resource(Token, '/token')
api.add_resource(Interest, '/interest')
api.add_resource(Profile, '/read_info')
api.add_resource(Theme, '/theme_list')
api.add_resource(Theme_News, '/<string:theme_name>/theme_news')
api.add_resource(Source,'/source')
api.add_resource(Search,'/<string:keyword>/<int:start>/<int:size>/search')

if __name__ == '__main__':
    app.run()
