"""
define app and routes
"""
from flask import Flask, Blueprint
from flask_restful import Resource, Api, url_for
from RealityServer.resourses.news import News

app = Flask(__name__)
api = Api(app)

api.add_resource(News, '/read')

if __name__ == '__main__':
    app.run()
