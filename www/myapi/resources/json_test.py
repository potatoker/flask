from flask_restful import Resource
from pymongo import MongoClient
from myapi.common.util import toJson
from flask import request


class PostTest(Resource):
    def post(self):
        pass
