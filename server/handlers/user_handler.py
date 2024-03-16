from quart import Blueprint, jsonify, request
from cerberus import Validator
from quart_jwt_extended import create_access_token
import bcrypt
import datetime
from db import db

new_user_schema = {
    'name': {'type': 'string', 'required': True},
    'email': {'type': 'string', 'required': True, 'regex': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'},
    'password': {'type': 'string', 'required': True, 'min': 6}
}

login_schema = {
    'email': {'type': 'string', 'required': True},
    'password': {'type': 'string', 'required': True}
}

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
async def register_user():
    try:
        user_data = await request.get_json()
        v = Validator(new_user_schema)
        if user_data is None or not v.validate(user_data):
            return jsonify({'message': 'Error data', 'errors': v.errors}), 400
        
        existing_user = db.users.find_one({'email': user_data['email']})
        if existing_user:
            return jsonify({'msg': 'User is exist'}), 400
        
        password = user_data['password'].encode('utf-8')
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        
        new_user_id = db.users.insert_one({'name': user_data['name'], 'email': user_data['email'], 'password': hashed_password}).inserted_id

        access_token = create_access_token(identity=str(new_user_id))

        return jsonify({'msg': 'Create user success', 'user': {'email': user_data['email'], 'name': user_data['name']}, 'access_token': access_token}), 201
        
    except Exception as e:
        return jsonify({'msg': 'Server Internal Error'}), 500
    
@user_bp.route('/login', methods=['POST'])
async def login_user():
    try:
        login_data = await request.get_json()
        v = Validator(login_schema)
        if login_data is None or not v.validate(login_data):
            return jsonify({'msg': 'Login information is wrong', 'errors': v.errors}), 400
        password = login_data['password'].encode('utf-8')
        existing_user = db.users.find_one({'email': login_data['email']})
        if bcrypt.checkpw(password, existing_user['password']):
            return jsonify({'msg': 'Login success', 'user': {'name': existing_user['name'], 'email': existing_user['email'], 'id': str(existing_user['_id'])}, 'access_token': create_access_token(identity=str(str(existing_user['_id'])), expires_delta=datetime.timedelta(days=30))}), 200
        return jsonify({'msg': 'Password is wrong'}), 400
    except Exception as e:
        return jsonify({'msg': 'Server Internal Error'}), 500