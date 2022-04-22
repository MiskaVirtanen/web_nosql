from flask import jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt
from bson.objectid import ObjectId
from models import User

class AccountRouteHandler(MethodView):
    @jwt_required()
    def get(self):
        logged_in_user = get_jwt()
        return jsonify(account=logged_in_user)
    
    @jwt_required()
    def patch(self):
         pass
        # TODO usernamen päivitys, tee erillinen dekoraattori tämän tarkistukseen  


class AccountHandler2(MethodView):
    jwt_required()
    def get(self):
        user_id = get_jwt()['sub']
        account = User.get_by_id(user_id)
        return jsonify(account=account.to_json())
