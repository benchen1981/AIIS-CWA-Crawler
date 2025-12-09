import requests
import json
import sqlite3
from database import init_db, save_weather_data, get_db_connection

# Using "Observation" dataset O-A0003-001 which has lat/lon
API_KEY = 'CWA-1FFDDAEC-161F-46A3-BE71-93C32C52829F'
DATASET_ID = 'O-A0003-001'
API_URL = f"https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/{DATASET_ID}?Authorization={API_KEY}&downloadType=WEB&format=JSON"

import urllib3

# Suppress only the single warning from urllib3 needed.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json'
    }
    # Do not catch exceptions here; let run_etl catch them so we get the specific error message
    # verify=False fixes the SSLError: [SSL: CERTIFICATE_VERIFY_FAILED]
    response = requests.get(API_URL, headers=headers, timeout=20, verify=False)
    response.raise_for_status()
    return response.json()

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
