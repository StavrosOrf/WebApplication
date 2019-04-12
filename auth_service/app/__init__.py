''' flask web_service with mongo '''
import os
import json
import datetime
from bson.objectid import ObjectId
from flask import Flask
from flask_pymongo import PyMongo
import connexion
from connexion import NoContent
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt


class JSONEncoder(json.JSONEncoder):
    ''' extend json-encoder class'''

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)



# # create the flask object
# app = Flask(__name__)

app = connexion.App(__name__)
app.add_api('auth.yaml')


# add mongo url to flask config, so that flask_pymongo can use it to make connection


# use the modified encoder class to handle ObjectId & datetime object while jsonifying the response.
app.app.json_encoder = JSONEncoder

app.app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET')
app.app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)


#from app.controllers import *