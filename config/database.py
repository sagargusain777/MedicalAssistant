from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
print(os.getenv("MONGODB_URI"))


client = MongoClient(MONGO_URI)

try:
    client.admin.command("ping")
    print("Connected to MongoDB server successfully")
except Exception as e:
    print(f"Error connecting to MongoDB server: {e}")


database = client[MONGO_DB_NAME]
users_collection = database["users"]

