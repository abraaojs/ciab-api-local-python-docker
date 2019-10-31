from flask_restful import fields, reqparse, inputs
    
class UserUtil():
    user_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'email': fields.String,
        'company': fields.String,
        'balance': fields.Integer,
        'order': fields.String,
        'embedding': fields.String
    }

    userParser = reqparse.RequestParser()
    userParser.add_argument('id', type=int, required=False)
    userParser.add_argument('name', type=str, required=True, help="This field must be a string!")
    userParser.add_argument('email', type=inputs.regex('^[a-zA-Z0-9]+(([\.\-\_][a-zA-Z0-9]+)?)+\@[a-zA-Z0-9]+\.[a-zA-Z0-9]+((\.[a-zA-Z0-9]+)?)+$'), help="This field must be a email format!")
    userParser.add_argument('company', type=str, required=True, help="This field must be a string!")
    userParser.add_argument('balance', type=int, required=True, help="This field must be a integer!")
    userParser.add_argument('order', type=str, required=False)
    userParser.add_argument('embedding', type=str, required=False)
