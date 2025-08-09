# Iosif Vieru
# 9 Aug. 2025

from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def get_database(db_name: str = None):
    global _client

    user = os.getenv('MONGO_USER')
    if not user:
        raise ValueError("MONGO_USER env variable not set.")

    password = os.getenv('MONGO_PASSWORD')
    if not password:
        raise ValueError('MONGO_PASSWORD env variable not set.')

    host = os.getenv('MONGO_HOST')
    if not host:
        raise ValueError('MONGO_HOST env variable not set.')

    app_name = os.getenv('MONGO_APP_NAME')
    if not app_name:
        raise ValueError('MONGO_APP_NAME env variable not set.')

    CONNECTION_STRING = f"mongodb+srv://{user}:{password}@{host}/?retryWrites=true&w=majority&appName={app_name}"

    # create connection using mongoclient
    client = MongoClient(CONNECTION_STRING)

    return client[db_name] if db_name else client

if __name__ == "__main__":
    client = get_database('camera_data')
    collection = client.get_collection('cameras')
    