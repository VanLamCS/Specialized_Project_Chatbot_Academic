import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')

db = None

try:
    client = MongoClient(MONGO_URI)
    db = client['chatbot_db']
    print("Connected to database")
except Exception as e:
    print("Error connecting to MongoDB:", e)