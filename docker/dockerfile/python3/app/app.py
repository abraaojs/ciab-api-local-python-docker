from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import os
from resources.userResource import User, UserEmail, UserList, UserTransfer, UserImage, UserSearchImage

MYSQL_USER = os.environ.get('MYSQL_USER')
MYSQL_PASS = os.environ.get('MYSQL_PASS')
MYSQL_HOST = os.environ.get('MYSQL_HOST')
MYSQL_DB = os.environ.get('MYSQL_DB')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + MYSQL_USER + ':' + MYSQL_PASS + '@' + MYSQL_HOST + '/' + MYSQL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
CORS(app, origins="*")

api.add_resource(User, '/users/<int:id>', endpoint='user')
api.add_resource(UserEmail, '/emails/<string:userEmail>', endpoint='email')
api.add_resource(UserList, '/users', endpoint='users')
api.add_resource(UserTransfer, '/users/<int:creditorId>/transfer/<int:debtorId>', endpoint='transfer')
api.add_resource(UserImage, '/users/<int:id>/image', endpoint='image')
api.add_resource(UserSearchImage, '/images', endpoint='images')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(host='0.0.0.0', port=5000)
