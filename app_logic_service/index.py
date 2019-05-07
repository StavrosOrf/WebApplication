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
import string
import random

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
SS1_URI = os.environ.get('SS1_URI')
SS2_URI = os.environ.get('SS2_URI')
app.app.config['MONGO_URI'] = os.environ.get('DB')
# app.app.config['MONGO_URI'] ="mongodb://localhost:27017/myDatabase"
SS1_URI = "http://storage_service1:4030"
SS2_URI = "http://storage_service2:4031"  
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
    print("auth_entry")
    URL = "http://auth_service:4020/api/authenticate/"
    myUrl = URL + my_email
    head = {'Authorization': 'Bearer {}'.format(token)}
    r = requests.get(myUrl, headers=head) 
    print(r)
    if r.status_code == 200 :
        return True
    else:
        return False
        


def decode_token(token):
    ''' Work-around to x-bearerInfoFunction required by connexion '''
    return {"token": token}

def id_generator(size=15, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))    


def get_all_users(email):

    #mongo.db.users.find(name)
    token = request.headers['Authorization'].split()[1]
    if not authenticate(email,token):
        return "Failed to authorize",401

    usr_list = []
    users = mongo.db.users.find()
    for usr in users:
        usr_list.append(usr['email']+" "+ usr['name'])
    return usr_list,200

def add_user():

    req_body = request.get_json() 
    email, name = req_body['email'], req_body['name']
    print(req_body)
    mongo.db.users.insert_one({'email': email,"name":name,"friends" : [],"galleries" : []})

    return "Succesfully created User",200 

def get_user(email):

    token = request.headers['Authorization'].split()[1]
    if not authenticate(email,token):
        return "Failed to authorize",401

    token = request.headers['Authorization'].split()[1]

    user = mongo.db.users.find_one({'email': email})

    if user:
        return jsonify({"name":user['name'],"email":user['email']}),200
    else:
        return "User not found",400

def get_all_friends():

    req_body = request.get_json() 
    my_email= req_body['my_email']

    token = request.headers['Authorization'].split()[1]
    if not authenticate(my_email,token):
        return "Failed to authorize",401
        
    user = mongo.db.users.find_one({'email': my_email})
    if user:
        friends = mongo.db.users.find_one( { 'email': my_email }, { 'friends' :1 })
       # print(glr_names['galleries'][1]['glr_name']) # a way to access glr names
        return friends,200 

    return "Failure",400

def add_friend():
    req_body = request.get_json() 
    my_email, friend_email = req_body['my_email'], req_body['friend_email']

    token = request.headers['Authorization'].split()[1]
    if not authenticate(my_email,token):
        return "Failed to authorize",401
        
    user = mongo.db.users.find_one({'email': my_email})
    friend = mongo.db.users.find_one({'email': friend_email})
    if user and friend:
        friend_name = friend['name']
        mongo.db.users.update( { 'email': my_email }, { '$push': { 'friends': { "email":friend_email,"name":friend_name } } })

        return"Succesfully addded Friend",200 

    return "Failure",400


    return "Success",200
def remove_friend(my_email,friend_email):
    token = request.headers['Authorization'].split()[1]
    if not authenticate(my_email,token):
        return "Failed to authorize",401

    user = mongo.db.users.find_one({'email': my_email})
    if user:
        mongo.db.users.update( { 'email': my_email }, { '$pull': { 'friends': { "email":friend_email } } })

        return"Succesfully removed Friend",200 

    return "Failure",400

def get_all_galleries(my_email):
    token = request.headers['Authorization'].split()[1]
    if not authenticate(my_email,token):
        return "Failed to authorize",401

    user = mongo.db.users.find_one({'email': my_email})
    if user:
        glr_names = mongo.db.users.find_one( { 'email': my_email }, { 'galleries.glr_name' :1 })
       # print(glr_names['galleries'][1]['glr_name']) # a way to access glr names
        return glr_names,200 

    return "Failure",400

def add_gallery():

    req_body = request.get_json() 
    email, glr_name = req_body['my_email'], req_body['glr_name']

    token = request.headers['Authorization'].split()[1]
    if not authenticate(email,token):
        return "Failed to authorize",401

    user = mongo.db.users.find_one({'email': email})
    if user:
        user = mongo.db.users.find_one({'email': email,"galleries.glr_name":glr_name})
        if not user:
            mongo.db.users.update( { 'email': email }, { '$push': { 'galleries': { "glr_name":glr_name,"Images":[] } } })
            return"Succesfully addded Gallery",200 
        return "Failure,gallery already exists",400
    return "Failure",400

def remove_gallery(my_email,glr_name):
    token = request.headers['Authorization'].split()[1]
    if not authenticate(my_email,token):
        return "Failed to authorize",401

    user = mongo.db.users.find_one({'email': my_email})
    if user:
        mongo.db.users.update( { 'email': my_email }, { '$pull': { 'galleries': { "glr_name":glr_name} } })

        return"Succesfully removed Gallery",200 

    return "Failure",400


def get_all_images():
    req_body = request.get_json() 
    email, glr_name = req_body['my_email'], req_body['glr_name']

    token = request.headers['Authorization'].split()[1]
    if not authenticate(email,token):
        return "Failed to authorize",401

    user = mongo.db.users.find_one({'email': email},{'galleries':{'$elemMatch': {"glr_name":glr_name}}})
    print(user)
    images = []
    # ss_uri = "1"
    if user:
        for image in user['galleries'][0]['Images']:
            if random.randint(1,2) == 1:
                ss_uri = image['ss1_uri']
            else:
                ss_uri = image['ss2_uri']

            ss_uri =  str(ss_uri).replace("storage_service1","localhost")
            ss_uri =  str(ss_uri).replace("storage_service2","localhost") 
            images.append(str(ss_uri)+"/api/image?img_id="+email+"."+image["access_token"]+".jpeg"+" "+str(image['img_name']))
                

        return images,200 

    return "Failure",400

def get_image(email,glr_name,img_name):
    token = request.headers['Authorization'].split()[1]
    if not authenticate(email,token):
        return "Failed to authorize",401
        
    user = mongo.db.users.find_one({'email': email},{'galleries':{'$elemMatch': {"glr_name":glr_name}}})
    print(user)
    if user:
        for image in user['galleries'][0]['Images']:
            
            if image['img_name'] == img_name:
                if random.randint(1,2) == 1:
                    ss_uri = image['ss1_uri']
                else:
                    ss_uri = image['ss2_uri']
                ss_uri =  ss_uri.replace("storage_service1","localhost")
                ss_uri =  ss_uri.replace("storage_service2","localhost")    
                return str(ss_uri)+"/api/image?img_id="+email+"."+image["access_token"]+".jpeg",200           
        

    return "Failure",400
    

def add_image():

    my_email, glr_name = request.form['my_email'], request.form['glr_name']
    img_name, img = request.files['img'].filename,request.files['img']
    img_name = request.form['img_name']
    token = request.headers['Authorization'].split()[1]
    if not authenticate(my_email,token):
        return "Failed to authorize",401
        
    user = mongo.db.users.find_one({'email': my_email,"galleries.glr_name":glr_name})
    if user:
        if mongo.db.users.find_one({'email': my_email,"galleries.glr_name":glr_name,"galleries.Images.$.img_name":img_name}):
            return "Image name already exists",400

        ss_uri = [SS1_URI,SS2_URI] #get 2 random SService URI
        access_token = id_generator();

        files = [0,0]
        img.filename = my_email+"."+access_token
        for i in range(2): 
            URL = ss_uri[i] + "/api/image"
            files[i] = {'img': (my_email+"."+access_token+".jpeg",img,'multipart/form-data',{'Expires': '0'})}
            print(URL)
            r = requests.post(URL,files = files[i]) 
            print(img)
            if not r.ok:
                print(r)
                return "Failure on SS",400
        mongo.db.users.update( { 'email': my_email,'galleries.glr_name':glr_name }, { '$push': 
        { 'galleries.$.Images': { "img_name":img_name,"ss1_uri":ss_uri[0],"ss2_uri":ss_uri[1],"access_token":access_token,"Comments":[] } } })

        return"Succesfully addded Image",200 
        
    

def remove_image(my_email,glr_name,img_name):
    token = request.headers['Authorization'].split()[1]
    if not authenticate(my_email,token):
        return "Failed to authorize",401
        
    user = mongo.db.users.find_one({'email': my_email,"galleries.glr_name":glr_name})

    if user:
        user = mongo.db.users.find_one({'email': my_email},{'galleries':{'$elemMatch': {"glr_name":glr_name}}})
        uri = [0,0]
        for image in user['galleries'][0]['Images']:
             if image['img_name'] == img_name:
                access_token = image['access_token']
                uri[0] = image['ss1_uri']
                uri[1] = image['ss2_uri']

        
       
        for i in range(2): 
            URL = uri[i]+"/api/image?img_id=" + my_email+"."+access_token+".jpeg"
            r = requests.delete(URL) 
            if not r.ok:
                print(r)
                return "Failure on SS",400
        mongo.db.users.update( { 'email': my_email,'galleries.glr_name':glr_name }, { '$pull': { 'galleries.$.Images': { "img_name":img_name }}})
        return "Successfully deleted image",200
    return "Failure",400 


def get_comments():
    return "Success",200

def add_comment(id):

    # req_body = request.get_json() 
    # email, glr_name = req_body['email'], req_body['glr_name']
    # img_name, comment = req_body['img_name'], req_body['comment']
    # user_name = req_body['user_name']

    # user = mongo.db.users.find_one({'email': email,"galleries.glr_name":glr_name,'galleries.Images.img_name':img_name})
    # print(user)
    # if user:

    #     comm_id = id_generator();
    #     mongo.db.users.update( { 'email': email,'galleries.glr_name':glr_name,'galleries.Images.img_name':img_name }, 
    #         { '$push':{ 'galleries.$[0].Images.$[1].Comments': { "commend_id": comm_id,"user": user_name,"comment":comment } } },
    #     {arrayFilters: [ { "galleries.glr_name":glr_name }]})

    return "Success",200


def remove_comment(id):
    return "Success",200
def edit_comment(id):
    return "Success",200

#application = app.app
if __name__ == '__main__':
    #LOG.info('running environment: %s', os.environ.get('ENV'))
    app.run(port=PORT)
    #app.config['DEBUG'] = os.environ.get('ENV') == 'development' # Debug mode if development env
#app.run(host='0.0.0.0', port=int(PORT)) # Run the app
#WS S Sapp.run(host='0.0.0.1', port=int(PORT))


