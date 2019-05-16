import os
import sys
import requests
from flask import jsonify, request, make_response, send_from_directory,send_file
from kazoo import client as kz_client
import logging

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
os.environ.update({'ROOT_PATH': ROOT_PATH})
sys.path.append(os.path.join(ROOT_PATH, 'modules'))
from app import app

PORT = os.environ.get('PORT')

NODE_PATH = "/web"
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

@app.errorhandler(404)
def not_found(error):
    """ error handler """
    return send_from_directory('UI', '404.html')

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

    return send_from_directory('UI', 'index.html')

@app.route('/login')
def serve_login():
    """ static files serve """
    return send_from_directory('UI','login.html')

@app.route('/register')
def serve_register():
    """ static files serve """
    return send_from_directory('UI','register.html')

@app.route('/index.css')
def serve_index_css():
    """ static files serve """
    return send_from_directory('UI','index.css')

@app.route('/index.js')
def serve_index_js():
    """ static files serve """
    return send_from_directory('UI','index.js')
@app.route('/favicon.ico')
def serve_favicon():
    """ static files serve """
    return send_file('./UI/favicon.ico')

@app.route('/<path:path>')
def static_proxy(path):
    """ static folder serve """
    file_name = path.split('/')[-1]
    dir_name = os.path.join('dist', '/'.join(path.split('/')[:-1]))
    return send_from_directory(dir_name, file_name)

@app.route('/test')
def test():
    return send_from_directory('UI','test.html')

if __name__ == '__main__':

    app.config['DEBUG'] = os.environ.get('ENV') == 'development' # Debug mode if development env
app.run(host='0.0.0.0', port=int(PORT)) # Run the app
