''' controller and routes for users '''
import os
from flask import request, jsonify
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
from app import app, mongo, flask_bcrypt, jwt
##from app.schemas import validate_user
#import logger

ROOT_PATH = os.environ.get('ROOT_PATH')
# LOG = logger.get_root_logger(__name__, filename=os.path.join(ROOT_PATH, 'output.log'))


@jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({
        'ok': False,
        'message': 'Missing Authorization Header'
    }), 401


#@app.app.route('/auth', methods=['POST'])
def auth_user(data):
    ''' auth endpoint '''
    #data = validate_user(request.get_json())
    if data['ok']:
        data = data['data']
        user = mongo.db.users.find_one({'email': data['email']}, {"_id": 0})
        LOG.debug(user)
        if user and flask_bcrypt.check_password_hash(user['password'], data['password']):
            del user['password']
            access_token = create_access_token(identity=data)
            refresh_token = create_refresh_token(identity=data)
            user['token'] = access_token
            user['refresh'] = refresh_token
            return jsonify({'ok': True, 'data': user}), 200
        else:
            return jsonify({'ok': False, 'message': 'invalid username or password'}), 401
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400


#@app.app.route('/register', methods=['POST'])
def register(name,email,password):
    ''' register user endpoint '''
    #data = validate_user(request.get_json())
    #if data['ok']:
    
    password = flask_bcrypt.generate_password_hash(data['password'])
    mongo.db.users.insert_one(name)
    mongo.db.users.insert_one(email)
    mongo.db.users.insert_one(password)
    return jsonify({'ok': True, 'message': 'User created successfully!'}), 200
    # else:
    #     return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400

# @app.app.route('/refresh', methods=['POST'])
# @jwt_refresh_token_required
# def refresh():
#     ''' refresh token endpoint '''
#     current_user = get_jwt_identity()
#     ret = {
#         'token': create_access_token(identity=current_user)
#     }
#     return jsonify({'ok': True, 'data': ret}), 200
def login():
 return jsonify({'ok': True, 'message': 'User created successfully!'}), 200

# @app.app.route('/user', methods=['GET', 'DELETE', 'PATCH'])
@jwt_required
def user():
    ''' route read user '''
    if request.method == 'GET':
        query = request.args
        data = mongo.db.users.find_one(query, {"_id": 0})
        return jsonify({'ok': True, 'data': data}), 200

    data = request.json()
    if request.method == 'DELETE':
        if data.get('email', None) is not None:
            db_response = mongo.db.users.delete_one({'email': data['email']})
            if db_response.deleted_count == 1:
                response = {'ok': True, 'message': 'record deleted'}
            else:
                response = {'ok': True, 'message': 'no record found'}
            return jsonify(response), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

    if request.method == 'PATCH':
        if data.get('query', {}) != {}:
            mongo.db.users.update_one(data['query'], {'$set': data.get('payload', {})})
            return jsonify({'ok': True, 'message': 'record updated'}), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400