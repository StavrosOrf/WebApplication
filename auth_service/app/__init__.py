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
from flask_cors import CORS


class JSONEncoder(json.JSONEncoder):
    ''' extend json-encoder class'''

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


app = connexion.App(__name__)
app.add_api('openapi.yaml')
cors = CORS(app.app)





# use the modified encoder class to handle ObjectId & datetime object while jsonifying the response.
app.app.json_encoder = JSONEncoder


# Debug
app.app.config['JWT_SECRET_KEY'] = "ironman"
app.app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)


