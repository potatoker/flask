from flask import request
from pymongo import MongoClient

from www.rest import data_test
from app import app

# app = Flask('rest')
client = MongoClient()
mydb = client.flask
my_collection = mydb.days


@app.route('/days/', methods=['Post'])
def get_one_day():
    day_id = request.form['day_id']
    one_day = my_collection.find_one({'day_id': day_id})

    if one_day:
        return data_test.toJson({'status': 'ok', 'data':one_day})
    else:
        return data_test.toJson({'status': 'no'})