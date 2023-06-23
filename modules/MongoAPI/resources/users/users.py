from bson import json_util
import json
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity
from modules.MongoAPI.app.blacklist import BLACKLIST
from modules.MongoAPI.models.users.users import UserModel
from pymongo.errors import WriteError
import hmac

attrib = reqparse.RequestParser()
attrib.add_argument('username', type=str, required=True, help="The field 'username' cannot be left blank.")
attrib.add_argument('password', type=str, required=True, help="The field 'password' cannot be left blank.")
attrib.add_argument('level', type=str)


class User(Resource):
    @jwt_required()
    def get(self, username):
        username_logged = get_jwt_identity()
        user_logged = UserModel.find_user_by_username(username_logged)

        user = UserModel.find_user_by_username(username)
        # criar uma função dentro de models/users para buscar o level do usuário
        if user_logged.get('level') == 'admin':
            if user:
                return json.loads(json_util.dumps(user))
        elif user_logged.get('level') == 'read':
            if user:
                return {"username": user.get('username')}
        return {"message": "User not found."}, 404

    @jwt_required()
    def delete(self, username):
        username_logged = get_jwt_identity()
        user_logged = UserModel.find_user_by_username(username_logged)

        user = UserModel.find_user_by_username(username)
        # criar uma função dentro de models/users para buscar o level do usuário
        if user_logged.get('level') == 'admin':
            if user:
                try:
                    UserModel.delete_user(username)
                except WriteError as e:
                    error = e.details['errmsg']
                    return {"message": "An error occurred trying to delete user.", "error": error}, 500
                return {"message": "User deleted."}
            return {"message": "User not found."}, 404
        return {"message": "Unauthorized login to 'delete' a user."}, 401


class UserRegister(Resource):
    # /cadastro
    @jwt_required()
    def post(self):
        username_logged = get_jwt_identity()
        user_logged = UserModel.find_user_by_username(username_logged)

        data = attrib.parse_args()
        if not data.get('level'):
            data['level'] = "read"

        # criar uma função dentro de models/users para buscar o level do usuário
        if user_logged.get('level') == 'admin':
            if UserModel.find_user_by_username(data['username']):
                return {"message": "The username '{}' already exists.".format(data['username'])}
            user = UserModel(**data)
            user.save_user()
            return {"message": "User created successfully!"}, 201
        elif user_logged.get('level') == 'read':
            return {"message": "Unauthorized login to 'create' a new user."}, 401


class UserLogin(Resource):
    def post(self):
        data = attrib.parse_args()

        user = UserModel.find_user_by_username(data['username'])

        if user and hmac.compare_digest(user['password'], data['password']):
            access_token = create_access_token(identity=user['username'])
            return {"access_token": access_token}, 200
        return {"message": "The username or password is incorrect."}, 401


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {"message": "Logged out successfully!"}, 200
