import pymongo
from django.conf import settings

def get_mongo_client():
    # Use default local connection if not specified
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    return client

def get_db():
    client = get_mongo_client()
    return client['educational_dropout_db']

def get_school_data_collection():
    db = get_db()
    return db['school_data']
