from flask import jsonify


class ChampionModel:
    from . champion_config import champions_collection

    def __init__(self, champion_id, key, name, title, full_name, icon, attack_type, resource, adaptive_type, stats, abilities, patch_last_changed):
        self.id = champion_id
        self.key = key
        self.name = name
        self.title = title
        self.full_name = full_name
        self.icon = icon
        self.resource = resource
        self.attack_type = attack_type
        self.adaptive_type = adaptive_type
        self.stats = stats
        self.abilities = abilities
        self.patch_last_changed = patch_last_changed

    def json(self):
        return {
            '_id': self.id,
            'key': self.key,
            'name': self.name,
            'title': self.title,
            'full_name': self.full_name,
            'icon': self.icon,
            'resource': self.resource,
            'attack_type': self.attack_type,
            'adaptive_type': self.adaptive_type,
            'stats': self.stats,
            'abilities': self.abilities,
            'patch_last_changed': self.patch_last_changed
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
            'key': self.key,
            'name': self.name,
            'title': self.title,
            'full_name': self.full_name,
            'icon': self.icon,
            'resource': self.resource,
            'attack_type': self.attack_type,
            'adaptive_type': self.adaptive_type,
            'stats': self.stats,
            'abilities': self.abilities,
            'patch_last_changed': self.patch_last_changed
        })
        return jsonify(self.json())

    def update_champion_by_id(self):
        champion = self.champions_collection.update_one({"_id": self.id}, {"$set": {
            '_id': self.id,
            'key': self.key,
            'name': self.name,
            'title': self.title,
            'full_name': self.full_name,
            'icon': self.icon,
            'resource': self.resource,
            'attack_type': self.attack_type,
            'adaptive_type': self.adaptive_type,
            'stats': self.stats,
            'abilities': self.abilities,
            'patch_last_changed': self.patch_last_changed
        }
        })
        return champion

    @classmethod
    def delete_champion_by_id(cls, champion_id):
        return cls.champions_collection.delete_one({"_id": champion_id})
