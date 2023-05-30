from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
mgdb = os.environ.get("MGDB_ATLAS")
client = MongoClient(mgdb)

db = client["mydatabase"]

user_collection = db["users"]