""" index file for REST APIs using Flask """
import os
import sys
import requests
from flask import jsonify, request, make_response, send_from_directory
from kazoo import client as kz_client
from flask import request
from flask_pymongo import PyMongo
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
from app import app
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
os.environ.update({'ROOT_PATH': ROOT_PATH})
sys.path.append(os.path.join(ROOT_PATH, 'modules'))

import connexion
from connexion import NoContent

#from logger import logger 

# Create a logger object to log the info and debug
#LOG = logger.get_root_logger(os.environ.get(
 #   'ROOT_LOGGER', 'root'), filename=os.path.join(ROOT_PATH, 'output.log'))

# Port variable to run the server on.
PORT = os.environ.get('PORT')

# my_client = kz_client.KazooClient('ZK')
 
# def my_listener(state):
#     if state == kz_client.KazooState.CONNECTED:
#         print("Client connected !")
 
# my_client.add_listener(my_listener)
# my_client.start(timeout=40)
# if app:
#     print('OK!!!!')

flask_bcrypt = Bcrypt(app.app)
jwt = JWTManager(app.app) 
# Docker
# app.app.config['MONGO_URI'] = os.environ.get('DB')
# Debug
app.app.config['MONGO_URI'] = "mongodb://localhost:27017/myDatabase"  
print("Connected to DEBUG mongodb")
mongo = PyMongo(app.app)

# @jwt.unauthorized_loader
# def unauthorized_response(callback):
#     return jsonify({
#         'ok': False,
#         'message': 'Missing Authorization Header'
#     }), 401


#@app.app.route('/auth', methods=['POST'])
def login():
    ''' auth endpoint '''
    #data = validate_user(request.get_json())
    #if data['ok']:
    
    req_body = request.get_json() 
    email, password = req_body['email'], req_body['password']

    user = mongo.db.reg_users.find_one({'email': email})
    if user and flask_bcrypt.check_password_hash(user['password'], password):
        token = create_access_token(identity=req_body)
        mongo.db.logged_in_users.insert_one({"email": email, "token": token})

        return jsonify({'token': token}), 200

#@app.app.route('/register', methods=['POST'])
def register():
    ''' register user endpoint '''
    #data = validate_user(request.get_json())
    #if data['ok']:
    req_body = request.get_json() 
    name, email, password  = req_body['name'], req_body['email'], req_body['password']
    password_hash = flask_bcrypt.generate_password_hash(password)
    # Insert registered user
    mongo.db.reg_users.insert_one({"name": name, "email": email, "password": password_hash})
    
    return "Successfully registered user", 200

# @app.app.route('/refresh', methods=['POST'])
# @jwt_refresh_token_required
# def refresh():
#     ''' refresh token endpoint '''
#     current_user = get_jwt_identity()
#     ret = {
#         'token': create_access_token(identity=current_user)
#     }
#     return jsonify({'ok': True, 'data': ret}), 200

# @app.app.route('/user', methods=['GET', 'DELETE', 'PATCH'])
# @jwt_required
# def user():
#     ''' route read user '''
#     if request.method == 'GET':
#         query = request.args
#         data = mongo.db.users.find_one(query, {"_id": 0})
#         return jsonify({'ok': True, 'data': data}), 200

#     data = request.json()
#     if request.method == 'DELETE':
#         if data.get('email', None) is not None: #             db_response = mongo.db.users.delete_one({'email': data['email']}) #             if db_response.deleted_count == 1:
#                 response = {'ok': True, 'message': 'record deleted'}
#             else:
#                 response = {'ok': True, 'message': 'no record found'}
#             return jsonify(response), 200
#         else:
#             return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

#     if request.method == 'PATCH':
#         if data.get('query', {}) != {}:
#             mongo.db.users.update_one(data['query'], {'$set': data.get('payload', {})})
#             return jsonify({'ok': True, 'message': 'record updated'}), 200
#         else:
#             return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

# @app.errorhandler(404)
# def not_found(error):
#     """ error handler """
#     #LOG.error(error)
#     return make_response(jsonify({'error': 'Not found'}), 404)


# @app.route('/')
# def index():
#     """ static files serve """
#     return send_from_directory('dist', 'index.html')


# @app.route('/<path:path>')
# def static_proxy(path):
#     """ static folder serve """
#     file_name = path.split('/')[-1]
#     dir_name = os.path.join('dist', '/'.join(path.split('/')[:-1]))
#     return send_from_directory(dir_name, file_name)


if __name__ == '__main__':
    #LOG.info('running environment: %s', os.environ.get('ENV'))
    app.run(os.environ.get('PORT'))
    #app.run(os.environ.get('PORT'))
    #app.app.config['DEBUG'] = os.environ.get('ENV') == 'development' # Debug mode if development env
#app.app.run(host='0.0.0.0', port=int(PORT)) # Run the app
