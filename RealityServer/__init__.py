"""
define app and routes
"""
from flask import Flask, Blueprint
from flask_restful import Resource, Api, url_for
from flask_pymongo import PyMongo
app = Flask(__name__, instance_relative_config=True)

app.config.from_object('config')
app.config.from_pyfile('config.py')

mongo = PyMongo(app)

from RealityServer.resourses.news import News
from RealityServer.resourses.media import Media
from RealityServer.resourses.user import Register
api = Api(app)
api.add_resource(News, '/read')
api.add_resource(Media, '/staroffice')
api.add_resource(Register, '/signup')

if __name__ == '__main__':
    app.run()
