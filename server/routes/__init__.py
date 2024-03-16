from quart import Blueprint
from handlers import user_bp, conversation_bp, message_bp

main_bp = Blueprint('main', __name__)

main_bp.register_blueprint(user_bp, url_prefix='/api/user')
main_bp.register_blueprint(conversation_bp, url_prefix='/api/conversation')
main_bp.register_blueprint(message_bp, url_prefix='/api/message')

__all__ = [
    'main_bp'
]