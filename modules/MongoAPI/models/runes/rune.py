from flask import jsonify


class RuneModel:
    from . rune_config import runes_collection

    def __init__(self,
                 rune_id: int,
                 name: str,
                 is_keystone: bool,
                 is_shard: bool,
                 description: str,
                 tree_path: str,
                 tier: int,
                 version: str):
        self.rune_id = rune_id
        self.name = name
        self.is_keystone = is_keystone
        self.is_shard = is_shard
        self.description = description
        self.tree_path = tree_path
        self.tier = tier
        self.version = version

    def json(self):
        return {
            "_id": self.rune_id,
            "name": self.name,
            "is_keystone": self.is_keystone,
            "is_shard": self.is_shard,
            "description": self.description,
            "tree_path": self.tree_path,
            "tier": self.tier,
            "version": self.version
        }

    @classmethod
    def find_rune_by_id(cls, rune_id):
        rune = cls.runes_collection.find({"_id": rune_id})
        if rune:
            return rune
        return None

    @classmethod
    def find_rune_by_name(cls, rune_name):
        rune = cls.runes_collection.find_one({'name': rune_name})
        if rune:
            return rune
        return None

    @classmethod
    def find_all_runes(cls):
        runes = list(cls.runes_collection.find())
        if runes:
            return runes
        return None

    def save_rune(self):
        self.runes_collection.insert_one({
            "_id": self.rune_id,
            "name": self.name,
            "is_keystone": self.is_keystone,
            "is_shard": self.is_shard,
            "description": self.description,
            "tree_path": self.tree_path,
            "tier": self.tier,
            "version": self.tier
        })

    def update_rune_by_id(self):
        rune = self.runes_collection.update_one({"_id": self.rune_id}, {"$set": {
            "_id": self.rune_id,
            "name": self.name,
            "is_keystone": self.is_keystone,
            "is_shard": self.is_shard,
            "description": self.description,
            "tree_path": self.tree_path,
            "tier": self.tier,
            "version": self.version
        }
        })
        return rune

    @classmethod
    def delete_rune_by_id(cls, rune_id):
        return cls.runes_collection.delete_one({'_id': rune_id})
