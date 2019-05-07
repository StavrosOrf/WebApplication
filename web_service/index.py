""" index file for REST APIs using Flask """
import os
import sys
import requests
from flask import jsonify, request, make_response, send_from_directory
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
# my_client.start(timeout=5)
if app:
    print('OK!!!!')
@app.errorhandler(404)
def not_found(error):
    """ error handler """
    #LOG.error(error)
    return make_response(jsonify({'error': 'Not found'}), 404)

def authenticate(my_email, token):
    URL = "http://auth_service:4020/api/authenticate/"
    myUrl = URL + my_email
    head = {'Authorization': 'Bearer {}'.format(token)}
    r = requests.get(myUrl, headers=head) 
    print(r)
    if r.status_code == 200 :
        return True
    else:
        return False

@app.route('/')
def serve_home():
    """ static files serve """
    if 'Email' in request.headers and 'Authorization' in request.headers:
        my_email = request.headers['Email']
        token = request.headers['Authorization'].split()[1];
        token_is_valid = authenticate(my_email, token)
        if (not token) or (not token_is_valid):
            return send_from_directory('UI', 'login.html')
        elif token_is_valid:
            return send_from_directory('UI', 'index.html')
    return send_from_directory('UI', 'login.html')

@app.route('/register')
def serve_register():
    """ static files serve """
    return send_from_directory('UI','register.html')

@app.route('/<path:path>')
def static_proxy(path):
    """ static folder serve """
    file_name = path.split('/')[-1]
    dir_name = os.path.join('dist', '/'.join(path.split('/')[:-1]))
    return send_from_directory(dir_name, file_name)

if __name__ == '__main__':
    #LOG.info('running environment: %s', os.environ.get('ENV'))
    app.config['DEBUG'] = os.environ.get('ENV') == 'development' # Debug mode if development env
app.run(host='0.0.0.0', port=int(PORT)) # Run the app
