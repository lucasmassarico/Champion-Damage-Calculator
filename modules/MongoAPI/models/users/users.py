from flask import jsonify
import json
from bson.objectid import ObjectId
from bson import json_util


class UserModel:
    from .users_config import users_collection

    def __init__(self, username, password, level):
        self.object_id = ObjectId()
        self.username = username
        self.password = password
        self.level = level

    def json(self):
        return {
            "_id": json.loads(json_util.dumps(self.object_id)),
            "username": self.username
        }

    @classmethod
    def find_user_by_username(cls, username):
        user = cls.users_collection.find_one({"username": username})
        if user:
            return user
        return None

    def save_user(self):
        self.users_collection.insert_one({
            "username": self.username,
            "password": self.password,
            "level": self.level
        })
        return jsonify(self.json())

    def update_user(self):
        user = self.users_collection.update_one({"username": self.username}, {'$set': {
            "username": self.username,
            "password": self.password,
            "level": self.level
        }
        })
        return user

    @classmethod
    def delete_user(cls, username):
        return cls.users_collection.delete_one({"username": username})
