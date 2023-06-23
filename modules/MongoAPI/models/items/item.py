from flask import jsonify


class ItemModel:
    from . item_config import items_collection

    def __init__(self,
                 item_id,
                 name,
                 tier,
                 rank,
                 buildsFrom,
                 buildsInto,
                 specialRecipe,
                 noEffects,
                 removed,
                 requiredChampion,
                 requiredAlly,
                 simpleDescription,
                 nicknames,
                 passives,
                 active,
                 stats,
                 shop
                 ):
        # DROP FROM MERAKI: iconOverlay, icon
        self.id = item_id
        self.name = name
        self.tier = tier
        self.rank = rank
        self.builds_from = buildsFrom
        self.builds_into = buildsInto
        self.special_recipe = specialRecipe
        self.no_effects = noEffects
        self.removed = removed
        self.required_champion = requiredChampion
        self.required_ally = requiredAlly
        self.simple_description = simpleDescription
        self.nicknames = nicknames
        self.passives = passives
        self.active = active
        self.stats = stats
        self.shop = shop

    def json(self):
        return {
            '_id': self.id,
            'name': self.name,
            'tier': self.tier,
            'rank': self.rank,
            'buildsFrom': self.builds_from,
            'buildsInto': self.builds_into,
            'specialRecipe': self.special_recipe,
            'noEffects': self.no_effects,
            'removed': self.removed,
            'requiredChampion': self.required_champion,
            'requiredAlly': self.required_ally,
            'simpleDescription': self.simple_description,
            'nicknames': self.nicknames,
            'passives': self.passives,
            'active': self.active,
            'stats': self.stats,
            'shop': self.shop
        }

    @classmethod
    def find_item_by_id(cls, item_id):
        item = cls.items_collection.find_one({"_id": item_id})
        if item:
            return item
        return None

    @classmethod
    def find_item_by_name(cls, item_name):
        item = cls.items_collection.find_one({'name': item_name})
        if item:
            return item
        return None

    @classmethod
    def find_all_items(cls):
        items = list(cls.items_collection.find())
        if items:
            return items
        return None

    def save_item(self):
        self.items_collection.insert_one({
            '_id': self.id,
            'name': self.name,
            'tier': self.tier,
            'rank': self.rank,
            'buildsFrom': self.builds_from,
            'buildsInto': self.builds_into,
            'specialRecipe': self.special_recipe,
            'noEffects': self.no_effects,
            'removed': self.removed,
            'requiredChampion': self.required_champion,
            'requiredAlly': self.required_ally,
            'simpleDescription': self.simple_description,
            'nicknames': self.nicknames,
            'passives': self.passives,
            'active': self.active,
            'stats': self.stats,
            'shop': self.shop
        })
        return jsonify(self.json())

    def update_item_by_id(self):
        item = self.items_collection.update_one({'_id': self.id}, {"$set": {
            '_id': self.id,
            'name': self.name,
            'tier': self.tier,
            'rank': self.rank,
            'buildsFrom': self.builds_from,
            'buildsInto': self.builds_into,
            'specialRecipe': self.special_recipe,
            'noEffects': self.no_effects,
            'removed': self.removed,
            'requiredChampion': self.required_champion,
            'requiredAlly': self.required_ally,
            'simpleDescription': self.simple_description,
            'nicknames': self.nicknames,
            'passives': self.passives,
            'active': self.active,
            'stats': self.stats,
            'shop': self.shop
        }
        })
        return item

    @classmethod
    def delete_item_by_id(cls, item_id):
        return cls.items_collection.delete_one({'_id': item_id})
