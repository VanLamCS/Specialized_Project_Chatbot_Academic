import os
from dotenv import load_dotenv
from quart import Quart
from quart_cors import cors
from quart_jwt_extended import JWTManager
from routes import main_bp

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
PORT = os.getenv('PORT') or 5000
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

app = Quart(__name__)

app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY

jwt = JWTManager(app)

app.register_blueprint(main_bp)
app = cors(app, allow_origin="*")  # Sử dụng '*' để cho phép tất cả các origin

if __name__ == "__main__":
    app.run(host='0.0.0.0', port = PORT)
