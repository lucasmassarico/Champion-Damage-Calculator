from modules.MongoAPI.models.db_config import *
from pymongo.errors import CollectionInvalid

collection_name = "items"

# test collection connection
try:
    db.validate_collection(collection_name)
except CollectionInvalid as err:
    print(err)

items_collection = db[collection_name]
