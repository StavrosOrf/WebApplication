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
import time

# Port variable to run the server on.
PORT = os.environ.get('PORT')
# Debug
# my_client = kz_client.KazooClient('ZK')
 
# def my_listener(state):
#     if state == kz_client.KazooState.CONNECTED:
#         print("Client connected !")
 
# my_client.add_listener(my_listener)
# # my_client.start(timeout=5)

this = sys.modules[__name__]
start_time = time.time()

this.TOTAL_READS = 0
this.TOTAL_WRITES = 0
this.TOTAL_DELETES = 0

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
img_dir = os.path.join(APP_ROOT, "images/")



def print_statistics():

    elapsed_time = time.time() - start_time
    print("=========Storage service report=================")
    print("Read requests per minute : "+str(this.TOTAL_READS/(elapsed_time)))
    print("Write/Deletes requests per minute : "+str((this.TOTAL_WRITES+this.TOTAL_DELETES)/(elapsed_time)))
    print("Working time:"+ str(elapsed_time))
    print("================================================")




def add_image():
    ''' upload image endpoint'''
    if not os.path.isdir(img_dir):
        os.mkdir(img_dir)
    
    # check if the post request has the file part
    if 'img' not in request.files:
        print('No img part')

    img_file = request.files['img'] 
    print(img_file)
    pathname = "/".join([img_dir, img_file.filename])
    img_file.save(pathname)


    this.TOTAL_WRITES += 1
    print_statistics()
    return "Successfully uploaded image.", 200

def get_image(img_id):
    ''' get image endpoint '''

    this.TOTAL_READS+=1
    print_statistics()
    return send_file(img_dir+img_id)

def remove_image(img_id):
    ''' remove image endpoint '''
    img_pathname = img_dir + img_id
    if os.path.exists(img_pathname):
        os.remove(img_pathname)
        
        this.TOTAL_DELETES += 1
        print_statistics()
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
