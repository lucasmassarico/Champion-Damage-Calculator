from ..db_config import *
from pymongo.errors import CollectionInvalid

collection_name = "users"

# test collection connection
try:
    db.validate_collection(collection_name)
except CollectionInvalid as err:
    print(err)

users_collection = db[collection_name]
