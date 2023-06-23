import os
from datetime import timedelta
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

secret_key = os.environ.get("SECRET_KEY")

app_port = 5999

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = secret_key
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
api = Api(app)
jwt = JWTManager(app)
