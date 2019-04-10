""" index file for REST APIs using Flask """
import os
import sys
import requests
from flask import jsonify, request, make_response, send_from_directory
from kazoo import client as kz_client
import logging
import connexion
from connexion import NoContent

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

def kati():
    return send_from_directory('dist', 'index.html')


# @app.route('/<path:path>')
# def static_proxy(path):
#     """ static folder serve """
#     file_name = path.split('/')[-1]
#     dir_name = os.path.join('dist', '/'.join(path.split('/')[:-1]))
#     return send_from_directory(dir_name, file_name)

def add_image1():

    return 'You send the message: {}'.format(message), 200
def get_image():

    return 'You send the message: {}'.format(message), 200

def remove_image():

    return 'You send the message: {}'.format(message), 200

def login():
    return "Success", 200

def register():
    return "Success", 200

def get_user():
    return "Success", 200

def get_all_friends():
    return "Success", 200

def add_friend():
    return "Success", 200

def remove_friend():
    return "Success", 200

def get_all_galleries():
    return "Success", 200

def add_gallery():
    return "Success", 200

def remove_gallery():
    return "Success", 200

def get_all_images():
    return "Success", 200

def get_all_users():
    return "Success", 200



def get_comments():
    return "Success", 200

def add_comment():
    return "Success", 200

def remove_comment():
    return "Success", 200

def edit_comment():
    return "Success", 200



#application = app.app
if __name__ == '__main__':
    #LOG.info('running environment: %s', os.environ.get('ENV'))
    app.run(port=4010)
    #app.config['DEBUG'] = os.environ.get('ENV') == 'development' # Debug mode if development env
#app.run(host='0.0.0.0', port=int(PORT)) # Run the app
#WS S Sapp.run(host='0.0.0.1', port=int(PORT))


