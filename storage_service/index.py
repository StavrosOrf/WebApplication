""" index file for REST APIs using Flask """
import os
import sys
import requests
from flask import jsonify,send_file, request, make_response, send_from_directory,render_template
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

# my_client = kz_client.KazooClient('ZK')
 
# def my_listener(state):
#     if state == kz_client.KazooState.CONNECTED:
#         print("Client connected !")
 
# my_client.add_listener(my_listener)
# # my_client.start(timeout=5)
# def get_image():

#     return "File successfully saved to "

# def remove_image():

#     return "File successfully saved to ."


# def add_image():
#     # if not request.files[]:
#     #     return  jsonify("wrong data"), 400
#     name = request.files['img_name']
#     img = request.files['img']

#     # if ext not in ('.png', '.jpg', '.jpeg'):
#     #     return "File extension not allowed."

#     save_path = "/images/{name}".format(name=name)


#     if not os.path.exists(save_path):
#         os.makedirs(save_path)

#     file_path = "{path}/{file}".format(path=save_path, file=name)
#     img.save(file_path)
#     return  jsonify("successfully saved"), 200


if app:
    print('OK!!!!')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    """ static files serve """
    return send_from_directory('dist', 'index.html')


@app.route("/add_image/<img_name>",methods=["POST"])
def upload(img_name):
    """ static folder serve """
    target = os.path.join(APP_ROOT,'images/')
    print(target)
    print(request.headers)
    if not os.path.isdir(target):
        os.mkdir(target)

    # for file in request.files.getlist("file"):
    file = request.files['file']
    print(file)
    filename = img_name
    print(img_name)
   
    destination = "/".join([target,filename])
    file.save(destination)

    return "SUCCESS",200


@app.route('/img/<filename>',methods=["GET","DELETE"])
def uploaded_file(filename):
    if request.method == 'GET':
        return send_file(os.path.join("../images/",filename))

    if request.method == 'DELETE':
        if os.path.exists(os.path.join(ROOT_PATH,"../images/",filename)):
          os.remove(os.path.join("../images/",filename))
          return "SUCCESS",200
        else:
          return("The file does not exist"),401 



if __name__ == '__main__':
    #LOG.info('running environment: %s', os.environ.get('ENV'))
    app.config['DEBUG'] = os.environ.get('ENV') == 'development' # Debug mode if development env
app.run(host='0.0.0.0', port=int(PORT)) # Run the app



# if __name__ == '__main__':
#     #LOG.info('running environment: %s', os.environ.get('ENV'))
#     # app.config['DEBUG'] = os.environ.get('ENV') == 'development' # Debug mode if development env
#     app.run(os.environ.get('PORT'))
#     flash('No file part')
