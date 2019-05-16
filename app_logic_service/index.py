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
from PIL import Image
from shutil import copyfileobj
from os import remove

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
os.environ.update({'ROOT_PATH': ROOT_PATH})
sys.path.append(os.path.join(ROOT_PATH, 'modules'))
from app import app

# Port variable to run the server on.
PORT = os.environ.get('PORT')
AUTH_PORT = os.environ.get('AUTH_PORT')
SS1_URI = os.environ.get('SS1_URI')
SS2_URI = os.environ.get('SS2_URI')
app.app.config['MONGO_URI'] = os.environ.get('DB')



# SS1_URI = "http://storage_service1:4030"
# SS2_URI = "http://storage_service2:4031"  
mongo = PyMongo(app.app)

NODE_PATH = "/app_logic"
kz = kz_client.KazooClient('ZK')

def get_SS_zk():

    SS_children = kz.get_children("/storage")
    print(SS_children)
    SS_values =[kz.get("/storage/"+child)[0] for child in SS_children]
    print(SS_values)
    return SS_values


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


def authenticate(token):
    print("auth_entry")
    URL = "http://auth_service:4020/api/authenticate"
    head = {'Authorization': 'Bearer {}'.format(token)}
    r = requests.get(URL, headers=head)
    # print(r)
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
    if not authenticate(token):
        resp = jsonify({'message': "Failed to authorize"})
        resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
        return resp, 401

    usr_list = []
    users = mongo.db.users.find()
    for usr in users:
        usr_list.append({"email":usr['email'],"name":usr['name']})
    resp = jsonify(usr_list)
    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
    return resp, 200  

def add_user():

    req_body = request.get_json() 
    email, name = req_body['email'], req_body['name']
    # print(req_body)
    mongo.db.users.insert_one({'email': email,"name":name,"friends" : [],"allowed_profiles" : [],"galleries" : []})

    return "Succesfully created User",200


def get_user(email):

    token = request.headers['Authorization'].split()[1]
    if not authenticate(token):
        resp = jsonify({'message': "Failed to authorize"})
        resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
        return resp, 401

    user = mongo.db.users.find_one({'email': email})

    if user:
        resp = jsonify({"name":user['name'],"email":user['email']})
        resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
        return resp, 200  
    else:
        resp = jsonify({'message':"User not found"})
        resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
        return resp, 400

def get_all_friends():

    req_body = request.get_json() 
    my_email= req_body['my_email']

    token = request.headers['Authorization'].split()[1]
    if not authenticate(token):
        resp = jsonify({'message': "Failed to authorize"})
        resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
        return resp, 401
        
    user = mongo.db.users.find_one({'email': my_email})
    if user:
        friends = mongo.db.users.find_one( { 'email': my_email }, { 'friends' :1,'allowed_profiles':1 })
       # print(glr_names['galleries'][1]['glr_name']) # a way to access glr names
        resp = jsonify(friends)
        resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
        return resp, 200

    resp = jsonify({'message': "Failure"})
    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
    return resp, 400

def add_friend():
    req_body = request.get_json() 
    my_email, friend_email = req_body['my_email'], req_body['friend_email']

    token = request.headers['Authorization'].split()[1]
    if not authenticate(token):
        resp = jsonify({'message': "Failed to authorize"})
        resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
        return resp, 401
        
    user = mongo.db.users.find_one({'email': my_email})
    friend = mongo.db.users.find_one({'email': friend_email})
    if user and friend:
        if mongo.db.users.find_one({'email': friend_email,'friends.email':friend_email}):
            resp = jsonify({'message': "Friend already added"})
            resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
            return resp, 400  

        friend_name = friend['name']
        mongo.db.users.update( { 'email': my_email }, { '$push': { 'friends': { "email":friend_email,"name":friend_name } } })
        mongo.db.users.update( { 'email': friend_email }, { '$push': { 'allowed_profiles': { "email":my_email ,"name":user['name']} } })

        resp = jsonify({'message': "Succesfully addded Friend"})
        resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
        return resp, 200  
   
    resp = jsonify({'message': "Failure"})
    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
    return resp, 400  

    return "Success",200

def remove_friend(my_email,friend_email):
    token = request.headers['Authorization'].split()[1]
    if not authenticate(token):
        resp = jsonify({'message': "Failed to authorize"})
        resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
        return resp, 401

    user = mongo.db.users.find_one({'email': my_email})
    friend = mongo.db.users.find_one({'email': friend_email})
    if user and friend:
        mongo.db.users.update( { 'email': my_email }, { '$pull': { 'friends': { "email":friend_email } } })
        mongo.db.users.update( { 'email': friend_email }, { '$pull': { 'allowed_profiles': { "email":my_email } } })

        resp = jsonify({'message': "Succesfully removed friend"})
        resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
        return resp, 200

    resp = jsonify({'message': "Failure"})
    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
    return resp, 400

def get_all_galleries(my_email):
    token = request.headers['Authorization'].split()[1]
    if not authenticate(token):
        resp = jsonify({'message': "Failed to authorize"})
        resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
        return resp, 401

    user = mongo.db.users.find_one({'email': my_email})
    if user:
        glr_names = mongo.db.users.find_one( { 'email': my_email }, { 'galleries.glr_name' :1 })
       # print(glr_names['galleries'][1]['glr_name']) # a way to access glr names
        resp = jsonify(glr_names)
        resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
        return resp, 200

    resp = jsonify({'message': "Failure"})
    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
    return resp, 400

def add_gallery():

    req_body = request.get_json() 
    email, glr_name = req_body['my_email'], req_body['glr_name']

    token = request.headers['Authorization'].split()[1]
    if not authenticate(token):
        resp = jsonify({'message': "Failed to authorize"})
        resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
        return resp, 401

    user = mongo.db.users.find_one({'email': email})
    if user:
        user = mongo.db.users.find_one({'email': email,"galleries.glr_name":glr_name})
        if not user:
            mongo.db.users.update( { 'email': email }, { '$push': { 'galleries': { "glr_name":glr_name,"Images":[] } } })

            resp = jsonify({'message': "Succesfully addded Gallery"})
            resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
            return resp, 200

        resp = jsonify({'message': "Failure,gallery already exists"})
        resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
        return resp, 400

    resp = jsonify({'message': "Failure"})
    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
    return resp, 400

def remove_gallery(my_email,glr_name):
    token = request.headers['Authorization'].split()[1]
    if not authenticate(token):
        resp = jsonify({'message': "Failed to authorize"})
        resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
        return resp, 401

    user = mongo.db.users.find_one({'email': my_email})
    if user:
        #ADD CHECK FOR GSLLERY EXISTENCE
        mongo.db.users.update( { 'email': my_email }, { '$pull': { 'galleries': { "glr_name":glr_name} } })

        resp = jsonify({'message': "Succesfully removed Gallery"})
        resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
        return resp, 200 

    resp = jsonify({'message': "Failure"})
    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
    return resp, 400


def get_all_images():
    req_body = request.get_json() 
    email, glr_name = req_body['my_email'], req_body['glr_name']

    token = request.headers['Authorization'].split()[1]
    if not authenticate(token):
        resp = jsonify({'message': "Failed to authorize"})
        resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
        return resp, 401

    user = mongo.db.users.find_one({'email': email},{'galleries':{'$elemMatch': {"glr_name":glr_name}}})
    # print(user)
    images = []
    # ss_uri = "1"
    if user:

        SS_children = get_SS_zk()

        for image in user['galleries'][0]['Images']:
            if image['ss1_uri'] not in SS_children and image['ss2_uri'] not in SS_children: 
                resp = jsonify({'message': "Failure"})
                resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
                return resp, 400
                
            if image['ss1_uri'] in SS_children and image['ss2_uri'] in SS_children:
                ss_uri = image['ss1_uri'] if (random.randint(1,2) == 1) else image['ss2_uri']
            elif image['ss1_uri'] in SS_children:
                ss_uri = image['ss1_uri']
            elif image['ss2_uri'] in SS_children:
                ss_uri = image['ss2_uri']

            ss_uri = "http://localhost:"+str(ss_uri.split(":")[2])

            images.append({
                            'link': str(ss_uri)+"/api/image?img_id="+email+"."+image["access_token"]+".jpeg",
                            'name':str(image['img_name'])
                          })
                

        resp = jsonify(images)
        #print(images);
        resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
        return resp, 200 

    resp = jsonify({'message': "Failure"})
    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
    return resp, 400

def get_image(email,glr_name,img_name):
    token = request.headers['Authorization'].split()[1]
    if not authenticate(token):
        resp = jsonify({'message': "Failed to authorize"})
        resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
        return resp, 401
        
    user = mongo.db.users.find_one({'email': email},{'galleries':{'$elemMatch': {"glr_name":glr_name}}})
    # print(user)
    if user:

        SS_children = get_SS_zk()

        for image in user['galleries'][0]['Images']:
            
            if image['img_name'] == img_name:
                                
                if image['ss1_uri'] not in SS_children and image['ss2_uri'] not in SS_children: 
                    resp = jsonify({'message': "Failure"})
                    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
                    return resp, 400
                
                if image['ss1_uri'] in SS_children and image['ss2_uri'] in SS_children:
                    ss_uri = image['ss1_uri'] if (random.randint(1,2) == 1) else image['ss2_uri']
                elif image['ss1_uri'] in SS_children:
                    ss_uri = image['ss1_uri']
                elif image['ss2_uri'] in SS_children:
                    ss_uri = image['ss2_uri']

                ss_uri = "http://localhost:"+str(ss_uri.split(":")[2])


                resp = jsonify((ss_uri)+"/api/image?img_id="+email+"."+image["access_token"]+".jpeg")
                resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
                return resp, 200            
        

    resp = jsonify({'message': "Failure"})
    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
    return resp, 400
    

def add_image():

    my_email, glr_name = request.form['my_email'], request.form['glr_name']
    img_name, img = request.files['img'].filename,request.files['img']
    img_name = request.form['img_name']

    token = request.form['token'].split()[1]
    if not authenticate(token):
        resp = jsonify({'message': "Failed to authorize"})
        resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
        return resp, 401
        
    user = mongo.db.users.find_one({'email': my_email,"galleries.glr_name":glr_name})
    if user:
        if mongo.db.users.find_one({'email': my_email,"galleries.glr_name":glr_name,"galleries.Images.img_name":img_name}):###------------
            resp = jsonify({'message': "Image name already exists!"})
            resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
            return resp, 400


        children = kz.get_children("/storage")
        ch_len = len(children)
        child = [None,None]

        _SS1 = ""
        _SS2 = ""

        if ch_len >1:
            child[0] = children.pop(random.randint(0, ch_len-1))
            child[1] = children.pop(random.randint(0, ch_len-2))

            _SS1 = kz.get("/storage/"+child[0])[0]
            _SS2 = kz.get("/storage/"+child[1])[0]
        elif ch_len == 1: 
            child[0] = children[0]
            _SS1 = kz.get("/storage/"+child[0])[0]
        else:
            print("No children!")
            resp = jsonify({'message': "Failure"})
            resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
            return resp, 400    


        ss_uri = [_SS1,_SS2] #get 2 random SService URI
        print(ss_uri)

        access_token = id_generator();

        img1 = img.stream.read()

        files = [0,0]
        img.filename = my_email+"."+access_token

        j = [0,1]
        if child[1] is None:
            j =[0]

        for i in j: 
            URL = str(ss_uri[i]) + "/api/image"
            print(URL)
            files[i] = {'img': (my_email+"."+access_token+".jpeg",img1,'multipart/form-data',{'Expires': '0'})}
            
            r = requests.post(URL,files = files[i]) 
            if not r.ok:
                resp = jsonify({'message': "Failure"})
                resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
                return resp, 400

        mongo.db.users.update( { 'email': my_email,'galleries.glr_name':glr_name }, { '$push': 
        { 'galleries.$.Images': { "img_name":img_name,"ss1_uri":ss_uri[0],"ss2_uri":ss_uri[1],"access_token":access_token,"Comments":[] } } })

        resp = jsonify({'message': "Succesfully added Image"})
        resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
        return resp, 200
        
    resp = jsonify({'message': "Failure"})
    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
    return resp, 400

def remove_image(my_email,glr_name,img_name):
    token = request.headers['Authorization'].split()[1]
    if not authenticate(token):
        resp = jsonify({'message': "Failed to authorize"})
        resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
        return resp, 401
        
    user = mongo.db.users.find_one({'email': my_email,"galleries.glr_name":glr_name})

    if user:
        user = mongo.db.users.find_one({'email': my_email},{'galleries':{'$elemMatch': {"glr_name":glr_name}}})
        uri = [0,0]
        access_token = ""
        for image in user['galleries'][0]['Images']:
             if image['img_name'] == img_name:
                access_token = image['access_token']
                uri[0] = image['ss1_uri']
                uri[1] = image['ss2_uri']
                print(uri)

        if access_token == "":
            resp = jsonify({'message': "Failure"})
            resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
            return resp, 400
        
        for i in range(2): 
            URL = str(uri[i])+"/api/image?img_id=" + str(my_email)+"."+str(access_token)+".jpeg"
            try:
                r = requests.delete(URL) 
                if not r.ok:
                    # print(r)
                    resp = jsonify({'message': "Failure"})
                    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
                    return resp, 400
            except Exception as e:
                pass


        mongo.db.users.update( { 'email': my_email,'galleries.glr_name':glr_name }, { '$pull': { 'galleries.$.Images': { "img_name":img_name }}})
        resp = jsonify({'message': "Succesfully deleted Image"})
        resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
        return resp, 200

    resp = jsonify({'message': "Failure"})
    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
    return resp, 400 


def get_comments(my_email):


    token = request.headers['Authorization'].split()[1]
    if not authenticate(token):
        resp = jsonify({'message': "Failed to authorize"})
        resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
        return resp, 401

    req_body = request.get_json() 
    email, glr_name = req_body['email'], req_body['glr_name']
    img_name = req_body['img_name']

    if not mongo.db.users.find_one({'email': email,"galleries.glr_name":glr_name,"galleries.Images.$.img_name":img_name}):

        comments = mongo.db.comments.find({'email':email,"glr_name":glr_name,"img_name":img_name})
        comm_list = []
        for comm in comments:
            comm_list.append({"comment":comm['comment'],"user_name":comm['user_name'],"id":comm['comm_id'],"email":comm['my_email']})
        resp = jsonify(comm_list)
        resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
        return resp, 200

    resp = jsonify({'message': "Failure"})
    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
    return resp, 400 

def add_comment(id,my_email):
    token = request.headers['Authorization'].split()[1]
    if not authenticate(token):
        resp = jsonify({'message': "Failed to authorize"})
        resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
        return resp, 401

    req_body = request.get_json() 
    email, glr_name = req_body['email'], req_body['glr_name']
    img_name, comment = req_body['img_name'], req_body['comment']
    user_name = req_body['user_name']

    user = mongo.db.users.find_one({'email': email},{'galleries':{'$elemMatch': {"glr_name":glr_name}}})
    #print(user)
    if user:
        for image in user['galleries'][0]['Images']:
        
            if image['img_name'] == img_name:
                comm_id = email +"."+id_generator()
                mongo.db.comments.insert_one({'email':email,'my_email':my_email,'comm_id': comm_id,"user_name":user_name,"glr_name":glr_name,"img_name":img_name,"comment" : comment})
                resp = jsonify({'message': "Succesfully added Comment",'id':comm_id})
                resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
                return resp, 200

    resp = jsonify({'message': "Failure"})
    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
    return resp, 400 


def remove_comment(id,my_email):
    token = request.headers['Authorization'].split()[1]
    if not authenticate(token):
        resp = jsonify({'message': "Failed to authorize"})
        resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
        return resp, 401

    mongo.db.comments.remove( {"comm_id":id})

    resp = jsonify({'message': "Success"})
    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
    return resp, 200

def edit_comment(id,my_email):
    token = request.headers['Authorization'].split()[1]
    if not authenticate(token):
        resp = jsonify({'message': "Failed to authorize"})
        resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
        return resp, 401

    comment = request.get_json()['comment']
    mongo.db.comments.update( {"comm_id":id},{"$set":{"comment":comment}})
    
    resp = jsonify({'message': "Success"})
    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:4000'
    return resp, 200


if __name__ == '__main__':

    app.run(port=PORT)


