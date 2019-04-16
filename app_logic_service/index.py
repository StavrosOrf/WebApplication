""" index file for REST APIs using Flask """
import os
import sys
import requests
from flask import jsonify, request, make_response, send_from_directory
from kazoo import client as kz_client
from flask import request
from flask_pymongo import PyMongo
import logging
import connexion
from connexion import NoContent
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
from flask_jwt_extended import JWTManager


ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
os.environ.update({'ROOT_PATH': ROOT_PATH})
sys.path.append(os.path.join(ROOT_PATH, 'modules'))
from app import app
#from logger import logger 

# Create a logger object to log the info and debug
#LOG = logger.get_root_logger(os.environ.get(
 #   'ROOT_LOGGER', 'root'), filename=os.path.join(ROOT_PATH, 'output.log'))

# Port variable to run the server on.
PORT = os.environ.get('PORT')
AUTH_PORT = os.environ.get('AUTH_PORT')
SS1_PORT = os.environ.get('SS1_PORT')
SS2_PORT = os.environ.get('SS2_PORT')

app.app.config['MONGO_URI'] = os.environ.get('DB')
print("Connected to DEBUG mongodb")
mongo = PyMongo(app.app)

#my_client = kz_client.KazooClient('ZK')
 
# def my_listener(state):
#     if state == kz_client.KazooState.CONNECTED:
#         print("Client connected !")
# logging.basicConfig()

# my_client.add_listener(my_listener)
# my_client.start(timeout=5)
if app:
    print('OK!!!!')
# @app.errorhandler(404)
# def not_found(error):
#     """ error handler """
#     #LOG.error(error)
#     return make_response(jsonify({'error': 'Not found'}), 404)


def authenticate(my_email,token):

    URL = "localhost:4020/api/authenticate/"
    my_email ="kati"
    myUrl = URL + my_email
    head = {'Authorization': 'token {}'.format(token)}

    r = requests.get(myUrl, headers=head) 

    if r :
        return True
    else:
        return False



def decode_token(token):
    ''' Work-around to x-bearerInfoFunction required by connexion '''
    return {"token": token}


def get_all_users():
    # print("TEST")
    # mongo.db.users.find(name)
    token = request.headers['Authorization'].split()[1]
    if authenticate(requests.email,token):
        return "Failed to authorize",201

    return "Success",200


def get_user():
    #authenticate

    return "Success",200

def get_all_friends():
    return "Success",200
def add_friend():
    return "Success",200
def remove_friend(): 
    return "Success",200
def get_all_galleries():
    return "Success",200
def add_gallery():
    return "Success",200
def remove_gallery():
    return "Success",200
def get_all_images():
    return "Success",200
def get_image():
    return "Success",200
def add_image():
    return "Success",200
def remove_image():
    return "Success",200
def get_comments():
    return "Success",200
def add_comment():
    return "Success",200
def remove_comment():
    return "Success",200
def edit_comment():
    return "Success",200

#application = app.app
if __name__ == '__main__':
    #LOG.info('running environment: %s', os.environ.get('ENV'))
    app.run(port=PORT)
    #app.config['DEBUG'] = os.environ.get('ENV') == 'development' # Debug mode if development env
#app.run(host='0.0.0.0', port=int(PORT)) # Run the app
#WS S Sapp.run(host='0.0.0.1', port=int(PORT))


