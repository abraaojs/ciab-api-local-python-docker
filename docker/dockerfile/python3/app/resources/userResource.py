from flask import request
from flask_restful import Resource, reqparse, marshal_with
from models.userModel import UserModel
from util.userUtil import UserUtil
from services.faceRecognitionService import FaceRecognition 
from exceptions.userException import UserException

class User(Resource):
    def get(self, id):
        user = UserModel.findById(id)
        if not user:
            UserException.responseError(404, 'User not found')
        return  user.json()

    @marshal_with(UserUtil.user_fields)
    def put(self, id):
        if not UserModel.findById(id):
            UserException.responseError(404, 'User not found')

        data = UserUtil.userParser.parse_args() 
        user = UserModel(id, data['name'], data['email'], data['company'], data['balance'], data['order'], data['embedding'])

        result = UserModel.findByEmail(user.email)
        if result and result['Users_id'] != id:
            UserException.responseError(409, 'Email already exist')

        try:
            user.update(id)
        except:
            UserException.responseError(500, 'An error occurred during data update')
        return user.json()

class UserEmail(Resource):
    def get(self, userEmail):
        user = UserModel.findByEmail(userEmail)
        if not user:
            UserException.responseError(404, 'User not found')
        return  user

class UserList(Resource):
    def get(self):
        result = UserModel.findAll()
        users = []
        for user in result:
            obj = user.json()
            users.append(obj) 
        return {'users': users}

    def post(self):
        data = UserUtil.userParser.parse_args()
        user = UserModel(None, data['name'], data['email'], data['company'], data['balance'], data['order'], data['embedding'])

        if UserModel.findByEmail(user.email):
            UserException.responseError(409, 'Email already exist')

        try:
            user.save()
        except:
            UserException.responseError(500, 'An error occurred during data update')
        return user.json(), 201

class UserTransfer(Resource):
    def put(self, creditorId, debtorId):
        creditor = UserModel.findById(creditorId)
        debtor = UserModel.findById(debtorId)

        if not creditor or not debtor:
            UserException.responseError(404, 'User not found')

        result = UserModel.transfer(creditor, debtor)
        if not result:
            UserException.responseError(409, 'Creditor do not have enough balance')
        return result

class UserImage(Resource):
    def post(self, id):
        user = UserModel.findById(id)
        if not user:
            UserException.responseError(404, 'User not found')
        file = request.files['file']
        if not file:
            UserException.responseError(400, 'Bad Request - File was not informed')
        user.embedding = FaceRecognition.imageEncoding(file)
        embeddings = UserModel.findAllEmbedding()
        userId = FaceRecognition.compareImages(user.embedding, embeddings)
        if userId:
            UserException.responseError(409, 'User found - id: ' + str(userId))
        try:
            user.update(id)
        except:
            UserException.responseError(500, 'An error occurred during data update')
        return user.json(), 201

class UserSearchImage(Resource):
    def post(self):
        file = request.files['file']
        if not file:
            UserException.responseError(400, 'Bad Request - File was not informed')
        imageEncoding = FaceRecognition.imageEncoding(file)
        embeddings = UserModel.findAllEmbedding()
        id = FaceRecognition.compareImages(imageEncoding, embeddings)
        if id:
            user = UserModel.findById(id)
            return user.json()
        UserException.responseError(404, 'User not found')
