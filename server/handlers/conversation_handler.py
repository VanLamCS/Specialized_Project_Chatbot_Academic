from quart import Blueprint, jsonify, request
from cerberus import Validator
from quart_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId
from datetime import datetime
from utils.object_id import is_object_id
import pymongo
from db import db

conversation_bp = Blueprint('conversation', __name__)

new_conversation_schema = {
    'name': {'type': 'string', 'max': 500},
}
edit_conversation_name_schema = {
    'conversation_id': {'type': 'string', 'required': True},
    'name': {'type': 'string', 'required': True}
}
get_history_schema = {
    'conversation_id': {'type': 'string', 'required': True},
}
delete_conversation_schema = {
    'conversation_id': {'type': 'string', 'required': True}
}

@conversation_bp.route('/create', methods=['POST'])
@jwt_required
async def create_conversation():
    try:
        now = datetime.utcnow()
        con_data = await request.get_json()
        v = Validator(new_conversation_schema)
        if con_data is None or not v.validate(con_data):
            return jsonify({'msg': 'Wrong data', 'errors': v.errors}), 400
        current_user_id = get_jwt_identity()
        existing_user = db.users.find_one({'_id': ObjectId(current_user_id)})
        con_name = con_data['name'] if con_data['name'] else "Default conversation"
        if not existing_user:
            return jsonify({'msg': 'No authorization'}), 401
        new_con_id = db.conversations.insert_one({'user_id': ObjectId(current_user_id), 'name': con_name, 'timestamp': now}).inserted_id
        return jsonify({'msg': 'Create new conversation success', 'conversation_id': str(new_con_id), 'timestamp': now}), 201
    except Exception as e:
        return jsonify({'msg': 'Server Internal Error'}), 500

@conversation_bp.route('/get-mine', methods=['GET'])
@jwt_required
async def get_conversation():
    try: 
        page = int(request.args.get('page')) if request.args.get('page') else 1
        limit = int(request.args.get('limit')) if request.args.get('limit') else 50
        current_user_id = get_jwt_identity()
        conversations = db.conversations.find({'user_id': ObjectId(current_user_id), 'deleted': {'$ne': True}}).sort('timestamp', pymongo.DESCENDING).skip((page - 1) * limit).limit(limit)
        docs = [{'name': conv['name'], 'id': str(conv['_id']), 'timestamp': conv['timestamp']} for conv in conversations]
        return jsonify({'msg': "Retrieve success", 'data': docs}), 200
    except Exception as e:
        return jsonify({'msg': 'Server Internal Error'}), 500

@conversation_bp.route('/change-name', methods=['POST'])
@jwt_required
async def edit_conversation_name():
    try: 
        conv_data = await request.get_json()
        v = Validator(edit_conversation_name_schema)
        if conv_data is None or not v.validate(conv_data):
            return jsonify({'msg': 'Wrong data', 'errors': v.errors}), 400
        current_user_id = get_jwt_identity()
        existing_user = db.users.find_one({'_id': ObjectId(current_user_id)})
        if not existing_user:
            return jsonify({'msg': 'No authorization'}), 401
        after_data = db.conversations.find_one_and_update({'_id': ObjectId(conv_data['conversation_id']), 'deleted': {'$ne': True}}, {'$set': {'name': conv_data['name']}})
        print(after_data)
        return jsonify({'msg': "Change name success", 'new_name': conv_data['name']}), 200
    except Exception as e:
        return jsonify({'msg': 'Server Internal Error'}), 500
    
@conversation_bp.route('/history', methods=['GET'])
@jwt_required
async def get_conversation_history():
    try:
        conversation_id = request.args.get('conversation_id')
        is_id, obj_conversation_id = is_object_id(conversation_id)
        if not is_id:
            return jsonify({'msg': 'Invalid conversation id'}), 400
        existing_conversation = db.conversations.find_one({'_id': obj_conversation_id})
        if not existing_conversation:
            return jsonify({'msg': 'Invalid conversation'}), 400
        page = int(request.args.get('page')) if request.args.get('page') else 1
        limit = int(request.args.get('limit')) if request.args.get('limit') else 50
        current_user_id = get_jwt_identity()
        existing_user = db.users.find_one({'_id': ObjectId(current_user_id)})
        if not existing_user:
            return jsonify({'msg': 'Not authenticated'}), 403
        res = db.messages.find({'conversation_id': obj_conversation_id}).sort('timestamp', pymongo.DESCENDING).skip((page - 1) * limit).limit(limit)
        
        messages = [{'id': str(mess['_id']), 'message': mess['message'], 'sender': mess['sender'], 'timestamp': mess['timestamp']} for mess in res]
        return jsonify({'msg': 'History is retrieved success', 'data': messages}), 200
    except Exception as e:
        return jsonify({'msg': 'Server Internal Error'}), 500
    
@conversation_bp.route('/<conversation_id>', methods=['DELETE'])
@jwt_required
async def delete_conversation(conversation_id):
    try:
        is_id, obj_conversation_id = is_object_id(conversation_id)
        if not is_id:
            return jsonify({'msg': 'Invalid conversation id'}), 400
        existing_conversation = db.conversations.find_one({'_id': obj_conversation_id})
        print('check existing_conversation: ', existing_conversation)
        if not existing_conversation:
            return jsonify({'msg': 'Invalid conversation'}), 400
        current_user_id = get_jwt_identity()
        result = db.conversations.update_one({'user_id': ObjectId(current_user_id), '_id': ObjectId(conversation_id)}, {'$set': {'deleted': True}})
        if result.acknowledged and result.modified_count > 0:
            return jsonify({'msg': 'Delete success'}), 200
        return jsonify({'msg': 'Delete is not success'}), 400
    except Exception as e:
        return jsonify({'msg': 'Server Internal Error'}), 500
