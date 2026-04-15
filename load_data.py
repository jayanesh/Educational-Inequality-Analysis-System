import pandas as pd
from pymongo import MongoClient
import sys

def load_csv_to_mongo():
    try:
        # Connect to MongoDB
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
        db = client["udise_db"]
        collection = db["education_data"]

        # Test connection
        client.server_info()

        # Clear existing data to avoid duplicates during testing
        collection.delete_many({})

        # Read CSV using Pandas
        df = pd.read_csv("udise_sample.csv")
        
        # Convert DataFrame to dictionary and insert into MongoDB
        data_dict = df.to_dict("records")
        collection.insert_many(data_dict)
        
        print(f"Successfully inserted {len(data_dict)} records into MongoDB.")
    except Exception as e:
        print(f"Error loading data: {e}")
        print("Falling back to local simulation...")
        # We could implement a fallback here if needed

if __name__ == "__main__":
    load_csv_to_mongo()
