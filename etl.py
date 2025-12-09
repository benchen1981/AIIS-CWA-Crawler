import requests
import json
import sqlite3
from database import init_db, save_weather_data, get_db_connection

# Using "Observation" dataset O-A0003-001 which has lat/lon
API_KEY = 'CWA-1FFDDAEC-161F-46A3-BE71-93C32C52829F'
DATASET_ID = 'O-A0003-001'
API_URL = f"https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/{DATASET_ID}?Authorization={API_KEY}&downloadType=WEB&format=JSON"

def fetch_data():
    try:
        response = requests.get(API_URL, timeout=10) # Added timeout
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

# ... (parse_data remains the same)

def run_etl():
    print("Starting ETL process...")
    try:
        init_db() 
        
        data = fetch_data()
        if not data:
            print("No data fetched.")
            return "No data fetched from API"
            
        parsed = parse_data(data)
        print(f"Parsed {len(parsed)} records.")
        
        if parsed:
            save_weather_data(parsed)
            print("Data saved to database.")
            return "Success"
        else:
            return "No records parsed"
            
    except Exception as e:
        print(f"ETL failed: {e}")
        return f"ETL failed: {str(e)}"
    
    print("ETL completed.")
    return "Unknown error"

if __name__ == "__main__":
    run_etl()
