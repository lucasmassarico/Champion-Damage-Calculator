from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from modules.MongoAPI.models.champions.champion import ChampionModel
from pymongo.errors import WriteError


class Champions(Resource):
    def get(self):
        champions = ChampionModel.find_all_champions()
        if champions:
            return champions
        return {'message': "Don't have any 'champion' in collection."}


class Champion(Resource):
    attrib = reqparse.RequestParser()
    # attrib.add_argument('_id', type=int, required=True, help="The field '_id' cannot be blank.")
    attrib.add_argument('name', type=str, required=True, help="The field 'name' cannot be blank.")
    attrib.add_argument('resource', type=str, required=True, help="The field 'resource' cannot be blank.")
    attrib.add_argument('attackType', type=str, required=True, help="The field 'attackType' cannot be blank.")
    attrib.add_argument('adaptiveType', type=str, required=True, help="The field 'adaptiveType' cannot be blank.")
    attrib.add_argument('stats', type=dict, required=True, help="The field 'stats' cannot be blank.")
    attrib.add_argument('abilities', type=dict, required=True, help="The field 'abilities' cannot be blank.")

    def get(self, champion_id):
        champion = ChampionModel.find_champion_by_id(champion_id)
        if champion:
            return champion
        return {"message": "Champion not found."}, 404

    @jwt_required()
    def post(self, champion_id):
        if ChampionModel.find_champion_by_id(champion_id):
            return {"message": "Champion id '{}' already exists.".format(champion_id)}, 400
        data = Champion.attrib.parse_args()
        champion = ChampionModel(champion_id, **data)
        try:
            champion.save_champion()
        except WriteError as e:
            error = e.details['errmsg']
            return {"message": "An error occurred trying to 'create' champion.", "error": error}, 500
        return champion.json(), 201

    @jwt_required()
    def put(self, champion_id):
        data = Champion.attrib.parse_args()
        champion = ChampionModel(champion_id, **data)
        found_champion = ChampionModel.find_champion_by_id(champion_id)
        if found_champion:
            try:
                champion.update_champion_by_id()
                return champion.json(), 200
            except WriteError as e:
                error = e.details['errmsg']
                return {"message": "An error occurred trying to 'update' champion.", "error": error}, 500
        try:
            champion.save_champion()
        except WriteError as e:
            error = e.details['errmsg']
            return {"message": "An error occurred trying to 'create' champion.", "error": error}, 500
        return champion.json(), 201

    @jwt_required()
    def delete(self, champion_id):
        found_champion = ChampionModel.find_champion_by_id(champion_id)
        if found_champion:
            try:
                ChampionModel.delete_champion_by_id(champion_id)
            except WriteError as e:
                error = e.details['errmsg']
                return {"message": "An error occurred trying to 'delete' champion.", "error": error}, 500
            return {"message": "Champion deleted."}
        return {"message": "Champion not found."}, 404
