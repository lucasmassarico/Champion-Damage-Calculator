from flask import jsonify, render_template
from modules.MongoAPI.resources.items.item import *
from modules.MongoAPI.app.blacklist import BLACKLIST
from modules.MongoAPI.app.app_config import app, api, jwt, app_port


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@jwt.token_in_blocklist_loader
def verify_blacklist(self, token):
    return token['jti'] in BLACKLIST


@jwt.revoked_token_loader
def invalid_access_token(jwt_header, jwt_payload):
    return jsonify({"message": "You have been logged out."}), 401


api.add_resource(Champions, '/champions')
api.add_resource(Champion, '/champions/<int:champion_id>')

api.add_resource(User, '/users/<string:username>')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')

api.add_resource(Items, '/items')
api.add_resource(Item, '/items/<int:item_id>')

if __name__ == '__main__':
    app.run(debug=True, port=app_port)
