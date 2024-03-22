from dotenv import load_dotenv
import os
from quart import Quart
from quart_jwt_extended import JWTManager
from chatcore import chat_core
from routes import main_bp

load_dotenv()

PORT = os.environ.get('PORT')
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

# Init chat core

app = Quart(__name__)

app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY

jwt = JWTManager(app)

app.register_blueprint(main_bp)

if __name__ == "__main__":
    app.run(port = PORT)