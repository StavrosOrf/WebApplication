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
import logging

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
os.environ.update({'ROOT_PATH': ROOT_PATH})
sys.path.append(os.path.join(ROOT_PATH, 'modules'))

import connexion
from connexion import NoContent
from jwt import(encode,decode)

# Port variable to run the server on.
PORT = os.environ.get('PORT')

flask_bcrypt = Bcrypt(app.app)
jwt = JWTManager(app.app) 
# Docker
app.app.config['MONGO_URI'] = os.environ.get('DB')
mongo = PyMongo(app.app)

NODE_PATH = "/auth"
kz = kz_client.KazooClient('ZK')
 
def my_listener(state):
    if state == kz_client.KazooState.LOST:
        # Register somewhere that the session was lost
        print("State: LOST!")
    elif state == kz_client.KazooState.SUSPENDED:
        # Handle being disconnected from Zookeeper
        print("State: SUSPENDED!")
    else:
        print("State: CONNECTED!")

        print("END OF ELSE!")
      
def make_zk_node():
    try:
        print("In making parent_node")
        kz.ensure_path('/')
        parent_node = kz.create(NODE_PATH, b"root")
        print(parent_node)
        print("Try making parent_node: Success!")
    except Exception as e:
        print("Try making parent_node: Exception!")
    
    try:
        print("In making child_node")
        kz.ensure_path(NODE_PATH)
        app_logic_node = kz.create(NODE_PATH+"/"+PORT, ephemeral=True, value=b"a value")
        print(app_logic_node)
        print("Try making child_node: Success!")
    except Exception as e:
         print("Try making child_node: Exception!")

logging.basicConfig()

kz.add_listener(my_listener)
kz.start(timeout=60)

make_zk_node()


def decode_token(token):
    ''' Work-around to x-bearerInfoFunction required by connexion '''
    return {"token": token}

#@app.app.route('/auth', methods=['POST'])
def login():
    ''' auth login endpoint '''

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
    

if __name__ == '__main__':

    app.run(os.environ.get('PORT'))

