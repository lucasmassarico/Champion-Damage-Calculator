from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse, inputs
from modules.MongoAPI.models.items.item import ItemModel
from . util import *
from pymongo.errors import WriteError


class Items(Resource):
    def get(self):
        items = ItemModel.find_all_items()
        if items:
            return items
        return {'message': "Don't have any 'item' in collection."}


class Item(Resource):
    attrib = reqparse.RequestParser()
    attrib.add_argument('name', type=str, required=True, help="The 'name' field must be a 'string' and cannot be blank.")
    attrib.add_argument('tier', type=int, required=True, help="The 'tier' field must be a 'integer' and cannot be blank.")
    attrib.add_argument('rank', type=str, action='append', help="The 'rank' field must be an 'array' and cannot be blank.")
    attrib.add_argument('buildsFrom', type=int, action='append', help="The 'buildsFrom' field must be an 'array'.")
    attrib.add_argument('buildsInto', type=int, action='append', help="The 'buildsInto' field must be an 'array'.")
    attrib.add_argument('specialRecipe', type=int, help="The 'specialRecipe' field must be a 'integer'.")
    attrib.add_argument('noEffects', type=inputs.boolean, required=True, help="The 'noEffects' field must be a 'boolean' and cannot be blank.")
    attrib.add_argument('removed', type=inputs.boolean, help="The 'removed' field must be a 'boolean'.")
    attrib.add_argument('requiredChampion', type=str, help="The 'requiredChampion' field must be a 'string'.")
    attrib.add_argument('requiredAlly', type=str, help="The 'requiredAlly' field must be a 'string'.")
    attrib.add_argument('simpleDescription', type=str, help="The 'simpleDescription' field must be a 'string'.")
    attrib.add_argument('nicknames', type=str, action='append', help="The 'nicknames' field must be an 'array'.")
    attrib.add_argument('passives', type=validate_dict, action='append', help="The 'passives' field must be an 'array'.")
    attrib.add_argument('active', type=validate_dict, action='append', help="The 'active' field must be an 'array'.")
    attrib.add_argument('stats', type=validate_dict, required=True, help="The 'stats' field must be an 'dictionary' and cannot be blank.")
    attrib.add_argument('shop', type=validate_dict, required=True, help="The 'shop' field must be an 'dictionary' and cannot be blank.")

    def get(self, item_id):
        item = ItemModel.find_item_by_id(item_id)
        if item:
            return item
        return {"message": "Item not found."}, 404

    @jwt_required()
    def post(self, item_id):
        if ItemModel.find_item_by_id(item_id):
            return {"message": "Item id '{}' already exists.".format(item_id)}, 400

        data = Item.attrib.parse_args()
        item_valid_data = {item: data[item] for item in data if data[item] is not None}
        item_fields = normalize_fields(**item_valid_data)

        item = ItemModel(item_id, **item_fields)
        try:
            item.save_item()
        except WriteError as e:
            error = e.details['errmsg']
            return {"message": "An error occurred trying to 'create' item.", "error": error}, 500
        return item.json(), 201

    @jwt_required()
    def put(self, item_id):
        data = Item.attrib.parse_args()
        print(data)
        item_valid_data = {item: data[item] for item in data if data[item] is not None}
        item_fields = normalize_fields(**item_valid_data)
        print(item_fields)

        item = ItemModel(item_id, **item_fields)
        found_item = ItemModel.find_item_by_id(item_id)
        if found_item:
            try:
                item.update_item_by_id()
                return item.json(), 200
            except WriteError as e:
                error = e.details['errmsg']
                return {"message": "An error occurred trying to 'update' item.", "error": error}, 500
        try:
            item.save_item()
        except WriteError as e:
            error = e.details['errmsg']
            return {"message": "An error occurred trying to 'create' item.", "error": error}, 500
        return item.json(), 201

    @jwt_required()
    def delete(self, item_id):
        found_item = ItemModel.find_item_by_id(item_id)
        if found_item:
            try:
                ItemModel.delete_item_by_id(item_id)
            except WriteError as e:
                error = e.details['errmsg']
                return {"message": "An error occurred trying to 'delete' item.", "error": error}, 500
            return {"message": "Item deleted."}
        return {"message": "Item not found."}, 404
