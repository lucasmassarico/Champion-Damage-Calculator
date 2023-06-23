import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

username = os.environ.get("MONGODB_USER")
password = os.environ.get("MONGODB_PWD")
connection_string = f'mongodb+srv://{username}:{password}@cluster.5ougas6.mongodb.net/?retryWrites=true&w=majority'
db_name = "champion_calculator"


# connect to server
try:
    client = MongoClient(connection_string)
    client.server_info()
except ServerSelectionTimeoutError as err:
    raise err

# connect / create db
db = client[db_name]
