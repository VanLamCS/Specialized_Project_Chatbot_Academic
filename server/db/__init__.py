from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.environ.get('MONGO_URI')

db = None

try:
    client = MongoClient(MONGO_URI)
    db = client['chatbot_db']
    print("Connected to database")
except Exception as e:
    print("Error connecting to MongoDB:", e)