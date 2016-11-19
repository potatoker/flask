from flask import Flask
import flask_restful
from myapi.resources.days import GetOneDay
from myapi.resources.users import Login,SignUp
from myapi.resources.moments import PostMoment2, PostMoment,PostMoment3,GetMoments,PostExploreDay2,GetExploreDays,PostComment,PostExploreDay
from flask import send_file
from flask import request
from os.path import join


app = Flask(__name__)
api = flask_restful.Api(app)

api.add_resource(GetOneDay, '/days')
api.add_resource(Login, '/login')
api.add_resource(PostMoment3, '/moments')
api.add_resource(PostMoment, '/post_moment')
api.add_resource(GetMoments, '/all_moments')
api.add_resource(SignUp,'/sign_up')
api.add_resource(PostExploreDay2, '/post_explore2')
api.add_resource(PostExploreDay, '/post_explore')
api.add_resource(GetExploreDays, '/explore_days')
api.add_resource(PostComment, '/comment')


@app.route('/<path:filename>')
def get_image(filename):
    root = app.config.get('STATIC_ROOT', '')
    file_path = join(root, filename)
    return send_file(file_path, mimetype='image/jpg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
