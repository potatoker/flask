from flask_restful import Resource
from pymongo import MongoClient
from myapi.common.util import toJson
from flask import request


client = MongoClient()
mydb = client.flask
days_collection = mydb.days


class GetOneDay(Resource):

    def post(self):
        day_id = request.form['day_id']
        one_day = days_collection.find_one({'day_id': day_id})

        if one_day:
            return toJson({'status': 'ok', 'data':one_day})
        else:
            return toJson({'status': 'no'})





