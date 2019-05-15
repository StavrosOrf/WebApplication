""" index file for REST APIs using Flask """
import os
import sys
import requests
import json
from flask import jsonify, request, make_response, send_from_directory
from kazoo import client as kz_client
from flask import request
from flask_pymongo import PyMongo
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity,get_jwt_claims)
from app import app
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
os.environ.update({'ROOT_PATH': ROOT_PATH})
sys.path.append(os.path.join(ROOT_PATH, 'modules'))

import connexion
from connexion import NoContent
from jwt import(encode,decode)

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
app.app.config['MONGO_URI'] = os.environ.get('DB')
# Debug
#app.app.config['MONGO_URI'] = "mongodb://localhost:27017/myDatabase"  
print("Connected to DEBUG mongodb")
mongo = PyMongo(app.app)


def decode_token(token):
    ''' Work-around to x-bearerInfoFunction required by connexion '''
    return {"token": token}

#@app.app.route('/auth', methods=['POST'])
def login():
    ''' auth login endpoint '''
    #data = validate_user(request.get_json())
    #if data['ok']:
    req_body = request.get_json() 
    email, password = req_body['email'], req_body['password']
    user = mongo.db.reg_users.find_one({'email': email})

    
    
    if user and flask_bcrypt.check_password_hash(user['password'], password):
        # token = create_access_token(identity=req_body)
        token = encode(req_body,os.environ.get('SECRET'),algorithm='HS256')
        mongo.db.logged_in_users.insert_one({"email": email, "token": token})

        print(decode(token,os.environ.get('SECRET'),algorithms=['HS256']))
        resp = jsonify({'token': token})
        resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
        return resp, 200
    resp  = jsonify({'message': "Log in Failed"})
    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
    return resp, 400    


def logout(my_email):
    ''' logout user endpoint '''
    token = request.headers['Authorization'].split()[1]
    db_response = mongo.db.logged_in_users.delete_one({'email': my_email, 'token': token})
    if db_response.deleted_count == 1:
        resp = jsonify({'message': "Successfully logged out"})
        resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
        return resp, 200
    resp = jsonify({'message': "Log out Failed"})
    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
    return resp, 400    

#@app.app.route('/register', methods=['POST'])
def register():
    ''' register user endpoint '''

    req_body = request.get_json() 
    name, email, password  = req_body['name'], req_body['email'], req_body['password']
    password_hash = flask_bcrypt.generate_password_hash(password)
    # Insert registered user
    if mongo.db.reg_users.find_one({'email': email}):
        resp = jsonify({'message': "Failed to  registered user:Email already in use!!"})
        resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
        return resp, 400
    mongo.db.reg_users.insert_one({"name": name, "email": email, "password": password_hash})

    URL = "http://app_logic_service:4010/api/users/add"
    data = {"email":email,"name": name}
    headers = {'Content-Type':'application/json'}

    r = requests.post(URL,json = data) 

    if r.status_code!=200 :
        resp = jsonify({'message': "Failed to  registered user"})
        resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
        return resp, 400

    resp = jsonify({'message': "Successfully registered user"})
    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
    return resp, 200  

def authenticate():
    ''' auth request endpoint '''
    # Get token from "Authorization: Bearer <token>" part of header
    token = request.headers['Authorization'].split()[1]

    email = decode(token,os.environ.get('SECRET'),algorithms=['HS256'])['email'];
    logged_in_user = mongo.db.logged_in_users.find_one({'email': email, 'token': token})
    if logged_in_user:
        resp = jsonify({'message': "Successfully authenticated user"})
        resp.headers['Access-Control-Allow-Origin'] = '*' #'http://localhost:4000'
        return resp, 200  
    resp = jsonify({'message':"Failed to authenticate user"})
    resp.headers['Access-Control-Allow-Origin'] = '*' #'http://localhost:4000'
    return resp, 400      
    

    # if logged_in_user:
    #     return "Successfully authenticated user", 200
    # return "failed to authenticate user", 400
    
if __name__ == '__main__':
    #LOG.info('running environment: %s', os.environ.get('ENV'))
    app.run(os.environ.get('PORT'))
    #app.run(os.environ.get('PORT'))
    #app.app.config['DEBUG'] = os.environ.get('ENV') == 'development' # Debug mode if development env
#app.app.run(host='0.0.0.0', port=int(PORT)) # Run the app
