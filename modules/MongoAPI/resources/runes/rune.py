from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse, inputs
from modules.MongoAPI.models.runes.rune import RuneModel
from .util import *
from pymongo.errors import WriteError


class Items(Resource):
    def get(self):
        runes = RuneModel.find_all_runes()
        if runes:
            return runes
        return {'message': "Don't have any 'rune' in collection."}


class Rune(Resource):
    attrib = reqparse.RequestParser()
    attrib.add_argument('name', type=str, required=True, help="The 'name' field must be a 'string' and cannot be blank.")
    attrib.add_argument('is_keystone', type=inputs.boolean, help="The 'is_keystone' field must be a 'boolean' and cannot be blank.")
    attrib.add_argument('is_shard', type=inputs.boolean, required=True, help="The 'is_shard' field must be a 'boolean' and cannot be blank.")
    attrib.add_argument('description', type=str, help="The 'description' field must be a 'string'.")
    attrib.add_argument('tree_path', type=str, required=True, help="The 'tree_path' field must be a 'string'.")
    attrib.add_argument('tier', type=int, required=True, help="The 'tier' field must be an 'integer'.")
    attrib.add_argument('version', type=str, required=True, help="The 'version' field must be a 'string'.")

    def get(self, rune_id):
        rune = RuneModel.find_rune_by_id(rune_id)
        if rune:
            return rune
        return {"message": "Rune not found."}, 404

    @jwt_required()
    def post(self, rune_id):
        if RuneModel.find_rune_by_id(rune_id):
            return {"message": "Rune id '{}' already exists.".format(rune_id)}, 400

        data = Rune.attrib.parse_args()
        rune_valid_data = {item: data[item] for item in data if data[item] is not None}
        rune_fields = normalize_fields(**rune_valid_data)

        rune = RuneModel(rune_id, **rune_fields)
        try:
            rune.save_rune()
        except WriteError as e:
            error = e.details['errmsg']
            return {"message": "An error occurred trying to 'create' rune.", "error": error}, 500
        return rune.json(), 201

    @jwt_required()
    def put(self, rune_id):
        data = Rune.attrib.parse_args()
        print(data)
        rune_valid_data = {item: data[item] for item in data if data[item] is not None}
        rune_fields = normalize_fields(**rune_valid_data)
        print(rune_fields)

        rune = RuneModel(rune_id, **rune_fields)
        found_rune = RuneModel.find_rune_by_id(rune_id)
        if found_rune:
            try:
                rune.update_rune_by_id()
                return rune.json(), 200
            except WriteError as e:
                error = e.details['errmsg']
                return {"message": "An error occurred trying to 'update' rune.", "error": error}, 500
        try:
            rune.save_rune()
        except WriteError as e:
            error = e.details['errmsg']
            return {"message": "An error occurred trying to 'create' rune.", "error": error}, 500
        return rune.json(), 201

    @jwt_required()
    def delete(self, rune_id):
        found_rune = RuneModel.find_rune_by_id(rune_id)
        if found_rune:
            try:
                RuneModel.delete_rune_by_id(rune_id)
            except WriteError as e:
                error = e.details['errmsg']
                return {"message": "An error occurred trying to 'delete' rune.", "error": error}, 500
            return {"message": "Rune deleted."}
        return {"message": "Rune not found."}, 404
