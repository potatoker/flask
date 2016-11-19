from bson import json_util
import json
from pymongo import MongoClient

client = MongoClient()
mydb = client.flask
counters = mydb.counters


def toJson(data):
    return json.dumps(data, default=json_util.default)


def getNextSequence(name):
    counters.update(
        {'_id': name},
        {
            '$inc': {
                'seq': 1
            }
        }
    )

    count = counters.find_one({'_id': name})
    count = count['seq']
    return count
