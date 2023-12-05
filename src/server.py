from quart import Quart, jsonify, request
from config import context_config
from utils.BKViQuAModel import ViQuADModel
import constants

BKViQuA = ViQuADModel()

app = Quart(__name__)

class BadRequestException(Exception):
    pass

def _check_question_type(c_key: int):
    if c_key == -1:
        return True
    context_types = context_config.context_types
    for item in context_types:
        item['context_key'] == c_key
        return True
    return False

@app.before_request
async def before_request():
    if request.method == 'OPTIONS':
        return cors_after_request()

@app.after_request
async def after_request(response):
    return cors_after_request(response)

def cors_after_request(response=None):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '86400',  # 24 hours
    }
    if response:
        response.headers.extend(headers)
    else:
        return headers
    return response

@app.route('/api/question-types', methods=['GET'])
def get_question_types():
    question_types = context_config.context_types
    question_types.append({
            'context_key': -1,
            'title': 'Tất cả',
        })
    return jsonify({
        'status': 'success',
        'data': {
            'question_types': question_types
        },
        'message': 'Retrieve question types success',
        'status_code': 200
    }), 200

@app.route('/api/ask', methods=['POST'])
async def ask_question():
    try:
        request_data = await request.get_json()
        question_type = request_data['question_type']
        question = request_data['question']
        if 'question_type' not in request_data or 'question' not in request_data:
            raise BadRequestException('Lack of data')
        if not isinstance(question_type, int) or not _check_question_type(question_type):
            raise BadRequestException('Question type is invalid')
        if not isinstance(question, str):
            raise BadRequestException('Datatype of question is invalid')
        answer = BKViQuA.forward(question, question_type)
        return jsonify({
            'status': 'success',
            'data': {
                'answer': str(answer['text']),
                'point': float(answer['logit_score'])
            },
            'message': 'There is the answer',
            'status_code': 200,
        }), 200
    except BadRequestException as error:
        return jsonify({
            'status': 'error',
            'message': str(error),
            'status_code': 400
        }), 400
    except Exception as error:
        return jsonify({
            'status': 'error',
            'message': str(error),
            'status_code': 500
        }), 500


if __name__ == '__main__':
    app.run(port=constants.SERVER_PORT)