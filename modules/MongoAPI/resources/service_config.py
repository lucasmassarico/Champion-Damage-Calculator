import os
from modules.MongoAPI.app.app_config import app_port
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

db_user = os.environ.get("API_DB_LOGIN")
db_pass = os.environ.get("API_DB_PASSWORD")

# MERAKI API ENDPOINT
champions_meraki_endpoint = "https://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/champions.json"
items_meraki_endpoint = "http://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/items.json"

# ENDPOINTS MongoAPI
url_to_login = f"http://127.0.0.1:{app_port}/login"
url_to_champions = f"http://127.0.0.1:{app_port}/champions/"
url_to_items = f"http://127.0.0.1:{app_port}/items/"
