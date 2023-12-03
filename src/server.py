from quart import Quart, jsonify, request
from config import context_config
from utils.BKViQuAModel import ViQuADModel
import constants

app = Quart(__name__)

class BadRequestException(Exception):
    pass

def _check_question_type(c_key: int):
    context_types = context_config.context_types
    for item in context_types:
        item['context_key'] == c_key
        return True
    return False

@app.route('/api/question-types', methods=['GET'])
def get_question_types():
    question_types = context_config.context_types
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
        
        bkViQuA = ViQuADModel()
        answer =  bkViQuA.forward(question, question_type)

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