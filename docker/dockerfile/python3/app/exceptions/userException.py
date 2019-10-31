from flask import abort

class UserException():

    def responseError(status_code, msg):
            return abort(status_code, msg)
