from flask import jsonify


class ChampionModel:
    from . champion_config import champions_collection

    def __init__(self, champion_id, name, attackType, resource, adaptiveType, stats, abilities):
        self.id = champion_id
        self.name = name
        self.resource = resource
        self.attackType = attackType
        self.adaptiveType = adaptiveType
        self.stats = stats
        self.abilities = abilities

    def json(self):
        return {
            '_id': self.id,
            'name': self.name,
            'resource': self.resource,
            'attackType': self.attackType,
            'adaptiveType': self.adaptiveType,
            'stats': self.stats,
            'abilities': self.abilities
        }

    @classmethod
    def find_champion_by_id(cls, champion_id):
        champion = cls.champions_collection.find_one({"_id": champion_id})
        if champion:
            return champion
        return None

    @classmethod
    def find_champion_by_name(cls, champion_name):
        champion = cls.champions_collection.find_one({'name': champion_name})
        if champion:
            return champion
        return None

    @classmethod
    def find_all_champions(cls):
        champions = list(cls.champions_collection.find())
        if champions:
            return champions
        return None

    def save_champion(self):
        self.champions_collection.insert_one({
            '_id': self.id,
            'name': self.name,
            'resource': self.resource,
            'attackType': self.attackType,
            'adaptiveType': self.adaptiveType,
            'stats': self.stats,
            'abilities': self.abilities
        })
        return jsonify(self.json())

    def update_champion_by_id(self):
        champion = self.champions_collection.update_one({"_id": self.id}, {"$set": {
            '_id': self.id,
            'name': self.name,
            'resource': self.resource,
            'attackType': self.attackType,
            'adaptiveType': self.adaptiveType,
            'stats': self.stats,
            'abilities': self.abilities
        }
        })
        return champion

    @classmethod
    def delete_champion_by_id(cls, champion_id):
        return cls.champions_collection.delete_one({"_id": champion_id})
