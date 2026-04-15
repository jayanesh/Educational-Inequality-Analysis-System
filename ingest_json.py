import json
import random
from pymongo import MongoClient

def ingest_representative_data():
    try:
        # 1. Load the raw JSON
        with open('udise_representative.json', 'r') as f:
            raw_data = json.load(f)

        # 2. Extract and Flatten
        flattened_data = []
        for state_entry in raw_data['data']:
            state_name = state_entry['state_ut']
            for dist in state_entry['districts']:
                # Mapping and Simulation
                ptr = dist['pupil_teacher_ratio']
                elec = dist['electricity_access_percent']
                
                # Intelligent Simulation of Dropout Rates based on PTR and Infrastructure
                # We want a realistic correlation for the dashboard EDA
                base_dropout = (ptr / 8) + ((100 - elec) / 4)
                secondary_dropout = round(max(0.5, min(25.0, base_dropout + random.uniform(-2, 2))), 1)
                primary_dropout = round(secondary_dropout * 0.4, 1)

                flattened_item = {
                    "State": state_name,
                    "District": dist['district_name'],
                    "Year": "2022-23",
                    "Total_Enrollment": dist['total_students'],
                    "Boys_Enrollment": int(dist['total_students'] * 0.52), # Estimation
                    "Girls_Enrollment": int(dist['total_students'] * 0.48), # Estimation
                    "Dropout_Rate_Primary": primary_dropout,
                    "Dropout_Rate_Secondary": secondary_dropout,
                    "Pupil_Teacher_Ratio": ptr,
                    "Electricity_Percent": elec,
                    "Total_Schools": dist['total_schools']
                }
                flattened_data.append(flattened_item)

        # 3. Insert into MongoDB
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
        db = client["udise_db"]
        collection = db["education_data"]

        # Clear existing data and replace
        collection.delete_many({})
        if flattened_data:
            collection.insert_many(flattened_data)
            print(f"Successfully ingested {len(flattened_data)} records into MongoDB.")
            print(f"Covers {len(raw_data['data'])} States/UTs.")
        
    except Exception as e:
        print(f"Ingestion failed: {e}")

if __name__ == "__main__":
    ingest_representative_data()
