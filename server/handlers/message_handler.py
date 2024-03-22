from quart import Blueprint, jsonify, request
from cerberus import Validator
from quart_jwt_extended import jwt_required
from bson.objectid import ObjectId
from chatcore.create_answer import create_answer
from datetime import datetime
from db import db

message_bp = Blueprint('message', __name__)

message_schema = {
    'conversation_id': {'type': 'string', 'required': True},
    'message': {'type': 'string', 'required': True}
}


@message_bp.route('/send', methods=['POST'])
@jwt_required
async def send_message():
    try:
        req_time = datetime.utcnow()
        message_data = await request.get_json()
        print(message_data)
        v = Validator(message_schema)
        if message_data is None or not v.validate(message_data):
            return jsonify({'msg': 'Message is invalid', 'errors': v.errors}), 400
        request_message = message_data['message']
        conversation_id = message_data['conversation_id']
        # Fake message reponse
        response_message, score = create_answer(request_message)
        res_time = datetime.utcnow()

        # Save messages to database
        q_id = db.messages.insert_one({'conversation_id': ObjectId(conversation_id),'message': request_message, 'sender': 'human', 'timestamp': req_time}).inserted_id
        a_id = db.messages.insert_one({'conversation_id': ObjectId(conversation_id),'message': response_message, 'sender': 'bot', 'timestamp': res_time}).inserted_id

        # Save pair of question and answer
        await save_pair_qa(q_id=q_id, a_id=a_id)
        
        return jsonify({'msg': "Answer already 😢", 'answer': response_message}), 201
    except Exception as e:
        return jsonify({'msg': 'Server Internal Error', 'errors': e}), 500

async def save_pair_qa(q_id: ObjectId, a_id: ObjectId):
    try:
        record_id = db.qa_pairs.insert_one({'question_id': q_id, 'answer_id': a_id}).inserted_id
        return True, record_id
    except Exception as e:
        return False, None