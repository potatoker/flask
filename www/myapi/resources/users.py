from flask_restful import Resource
from pymongo import MongoClient
from flask import request,jsonify
from myapi.common.util import getNextSequence
import json
import random


client = MongoClient()
mydb = client.flask
users_collection = mydb.users



class Login(Resource):
    def post(self):

        email = request.form['email']
        pwd = request.form['pwd']

        find_user = users_collection.find({'email':email},{'_id':0})[0]
        dumb_user = users_collection.find()[0]
        dumb_user['uid']="-1"
        if pwd == find_user['pwd']:
            return jsonify(find_user)
        else:
            print(dumb_user)
            return jsonify(dumb_user)


class SignUp(Resource):
    def post(self):
        print("sb sign up")
        id = random.randint(0,1000)

        user = request.form['user']
        user = json.loads(user)

        print(user)

        photo_list=["https://img3.doubanio.com/icon/ul63847035-14.jpg","https://img3.doubanio.com/icon/ul58521972-11.jpg",
                    "https://img3.doubanio.com/view/photo/photo/public/p2373426056.jpg","https://img3.doubanio.com/view/photo/photo/public/p2324480246.jpg",
                    "https://img1.doubanio.com/view/photo/photo/public/p2324480188.jpg","https://img1.doubanio.com/view/photo/photo/public/p2324480177.jpg",
                    "https://img1.doubanio.com/view/photo/photo/public/p2324479749.jpg","https://img3.doubanio.com/view/photo/photo/public/p2324475245.jpg",
                    "https://img3.doubanio.com/view/photo/photo/public/p2324475062.jpg","https://img3.doubanio.com/view/photo/photo/public/p2324474996.jpg"]

        photo_id = random.randint(0,9)

        new_user = {
            'email':user['email'],
            'uid':id,
            'pwd':user['pwd'],
            'name':user['name'],
            'avatarurl':photo_list[photo_id],
            'avataruri':"",
            'currentdayid':"",
            'desc':"",
            'motto':""
        }

        users_collection.replace_one({"email":user['email']}, new_user, True)
        user = users_collection.find({'email':user['email']},{'_id':0})
        user = user[0]
        print(user)

        return jsonify(user)






