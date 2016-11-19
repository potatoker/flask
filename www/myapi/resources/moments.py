from flask_restful import Resource
from pymongo import MongoClient
from flask import request,jsonify
from myapi.common.util import getNextSequence
import json
import random
import os
from flask import Flask
from os.path import join


client = MongoClient()
mydb = client.flask
days_collection = mydb.moments
users_collection = mydb.users
explore_days = mydb.explores


class PostMoment2(Resource):
    def post(self):

        print(request.form)

        moment = request.form['moment']
        print(moment)

        moment = json.loads(moment)
        print(moment)

        day_id = request.form['day_id']
        print(day_id)
        moment_id = getNextSequence('moment')

        moment['_id'] = moment_id

        print(moment)

        # moment = toJson(moment)
        # print(moment)

        # days_collection.update(
        #     {'day_id': day_id},
        #     {'$push': {'moments': moment}}
        # )

        moments = days_collection.find(
            {'day_id': day_id},
            {'moments': 1, '_id': 0}
        )

        # moments = days_collection.find()

        # for i in moments:
        #     print i
        moments = moments[0]
        print(moments['moments'])

        # print(toJson(moments['moments']))
        print(jsonify(moments['moments']))

        return jsonify(moments['moments'])


class PostMoment3(Resource):

    def post(self):
        moment = request.form['moment']
        moment = json.loads(moment)

        # print(moment)
        # print(moment['moment_id'])


        moment_record = {
            "moment_id": moment['moment_id'],
            "photo_url": moment['photo_url'],
            "date":moment['date'],
            "desc":moment['desc'],
            "day_id":moment['day_id'],
            "location":moment['location'],
            "uid":moment['uid'],
            "img_string":moment['img_string'],
            "moment_snyc":moment['moment_snyc'],
            "fava_flag":moment['fava_flag']
        }

        days_collection.replace_one({"moment_id":moment['moment_id']}, moment_record, True)

        moments = days_collection.find({},{'_id':0})
        moments = list(moments)

        print(moments)

        # print(jsonify(moments))

        return jsonify(moments)


class GetMoments(Resource):

    def post(self):

        uid = request.form['uid']

        moments = days_collection.find({},{'_id':0})
        moments = list(moments)

        print(moments[0]['photo_url'])
        print(moments[0]['date'])
        print(moments[1]['photo_url'])
        print(moments[1]['date'])

        return jsonify(moments)


class GetTimeStamps(Resource):
    def post(self):
        uid = request.form['uid']

        stamps = days_collection.find({'uid': uid},{'date':1,'_id':0})

        stamps = list(stamps)

        return jsonify(stamps)



class GetExploreDays(Resource):
    def post(self):
        uid = request.form['uid']

        days = explore_days.find({},{'_id':0})
        days = list(days)
        return jsonify(days)


class PostExploreDay(Resource):
    def post(self):
        explore = request.form['explore_day']
        explore = json.loads(explore)
        explore_days.replace_one({"day_id":explore['day_id']}, explore, True)
        explore_day = explore_days.find({'day_id':explore['day_id']},{'day_id':1,'_id':0})
        return explore_day[0]['day_id']


class PostExploreDay2(Resource):
    def post(self):
        explore = request.form['explore_day']
        explore = json.loads(explore)

        app = Flask(__name__)
        root = app.config.get('STATIC_ROOT', '')

        for moment in explore['moments']:
            file_name = moment['uid']+ "_" + moment['moment_id'] +".jpg"
            file_path = join(root, file_name)
            print (file_path)
            # if not os.path.exists(file_path):
            #     os.makedirs(file_path)
            try:
                infile = open(file_path, 'wb')
            except IOError:
                raise

            infile.write(moment['img_string'].decode('base64'))
            infile.close()
            moment['remote_url'] = "http://119.29.138.234:5000/"+file_name
            moment['img_string'] = ""

        old_explore_day = explore_days.find({'day_id':explore['day_id']})
        old_explore_day = list(old_explore_day)
        if len(old_explore_day) >0:
            explore['comments'] = old_explore_day[0]['comments']
        explore_days.replace_one({"day_id":explore['day_id']}, explore, True)
        explore_day = explore_days.find({'day_id':explore['day_id']},{'day_id':1,'_id':0})
        return explore_day[0]['day_id']


class PostMoment(Resource):
    def post(self):
        moment = request.form['moment']
        moment = json.loads(moment)
        day_id = request.form['day_id']

        moment_id = getNextSequence('moment')
        moment['_id'] = moment_id

        days_collection.update(
            {'_id': day_id},
            {'$push': {'moments': moment}}
        )

        return 'ok'

class PostComment(Resource):
    def post(self):
        comment = request.form['comment']
        comment = json.loads(comment)
        day_id = comment['day_id']
        explore_days.update({'day_id':day_id},{'$push':{'comments':comment}})
        return "1"