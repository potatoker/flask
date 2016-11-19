from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import json_util
import json

app = Flask('rest')


client = MongoClient()
mydb = client.flask
user_collection = mydb.users
days_collection = mydb.days


def toJson(data):
    return json.dumps(data, default=json_util.default)


@app.route('/login/', methods=['POST'])
def login():
    email = request.form['email']
    pwd = request.form['pwd']
    user = user_collection.find_one({'email':email})

    if pwd == user['pwd']:
        return '1'
    else:
        return '0'


@app.route('/login2/', methods=['POST'])
def login2():
    email = request.form['email']
    user = user_collection.find_one({'email': email})

    print(user)
    if user:
        return toJson({'status': 'ok', 'data': user})
    else:
        return toJson({'status': 'no'})


@app.route('/days/', methods=['Post'])
def get_one_day():
    day_id = request.form['day_id']
    one_day = days_collection.find_one({'day_id': day_id})

    if one_day:
        return toJson({'status': 'ok', 'data':one_day})
    else:
        return toJson({'status': 'no'})


if __name__ == '__main__':
    app.run(debug=True)