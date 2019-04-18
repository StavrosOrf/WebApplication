""" index file for REST APIs using Flask """
import os
import sys
import requests
from flask import jsonify, send_file, request, make_response, send_from_directory,render_template
from kazoo import client as kz_client

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
# Debug
# my_client = kz_client.KazooClient('ZK')
 
# def my_listener(state):
#     if state == kz_client.KazooState.CONNECTED:
#         print("Client connected !")
 
# my_client.add_listener(my_listener)
# # my_client.start(timeout=5)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
img_dir = os.path.join(APP_ROOT, "images/")

def add_image():
    ''' upload image endpoint'''
    if not os.path.isdir(img_dir):
        os.mkdir(img_dir)
    
    # check if the post request has the file part
    if 'img' not in request.files:
        print('No img part')

    img_file = request.files['img'] 
    pathname = "/".join([img_dir, img_file.filename])
    img_file.save(pathname)

    return "Successfully uploaded image.", 200

def get_image(img_id):
    ''' get image endpoint '''
    return send_file(img_dir+img_id)

def remove_image(img_id):
    ''' remove image endpoint '''
    img_pathname = img_dir + img_id
    if os.path.exists(img_pathname):
        os.remove(img_pathname)
        return "SUCCESS", 200
    else:
        return "Failed. File does not exist", 401 

if __name__ == '__main__':
    #LOG.info('running environment: %s', os.environ.get('ENV'))
    # app.config['DEBUG'] = os.environ.get('ENV') == 'development' # Debug mode if development env
    app.app.run(host='0.0.0.0', port=int(PORT)) # Run the app

# if __name__ == '__main__':
#     #LOG.info('running environment: %s', os.environ.get('ENV'))
#     # app.config['DEBUG'] = os.environ.get('ENV') == 'development' # Debug mode if development env
#     app.run(os.environ.get('PORT'))
#     flash('No file part')
