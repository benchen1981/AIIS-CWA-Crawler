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

def parse_data(json_data):
    """
    Parse the CWA O-A0003-001 (Observation) JSON response.
    Structure: cwaopendata -> dataset -> Station
    Extracts: StationName (City/Town), AirTemperature, ObsTime, Lat, Lon.
    """
    parsed_items = []
    
    try:
        root = json_data.get('cwaopendata', {})
        dataset = root.get('dataset', {})
        stations = dataset.get('Station', [])

        for st in stations:
            # Geography
            geo = st.get('GeoInfo', {})
            town = geo.get('TownName', 'Unknown')
            city = geo.get('CountyName', 'Unknown')
            
            # Coordinates
            coords = geo.get('Coordinates', [])
            lat = 0.0
            lon = 0.0
            if coords:
                # Prefer TWD67 or WGS84? WGS84 is usually standard for web maps.
                # The debug structure showed both.
                # Let's verify format. Usually index 1 is WGS84 based on debug output order?
                # Actually let's look for CoordinateName='WGS84'
                for coord in coords:
                    if coord.get('CoordinateName') == 'WGS84':
                        lat = float(coord.get('StationLatitude', 0))
                        lon = float(coord.get('StationLongitude', 0))
                        break
                # Fallback if loop didn't find specific name
                if lat == 0 and coords:
                     lat = float(coords[0].get('StationLatitude', 0))
                     lon = float(coords[0].get('StationLongitude', 0))

            # Weather Elements
            # O-A0003-001 uses 'WeatherElement' (dict) or list?
            # Debug script showed: WeatherElement keys: dict_keys(['Weather', ... 'AirTemperature'])
            # So it is a dict.
            wes = st.get('WeatherElement', {})
            temp_val = wes.get('AirTemperature')
            
            # ObsTime
            obs_time = st.get('ObsTime', {}).get('DateTime', '')

            # Convert temp to float safely
            try:
                final_temp = float(temp_val) if temp_val else None
            except ValueError:
                final_temp = None

            if final_temp is not None:
                parsed_items.append({
                    'city': city,
                    'town': town,
                    'temperature': final_temp,
                    'obs_time': obs_time,
                    'latitude': lat,
                    'longitude': lon
                })
                
    except Exception as e:
        print(f"Error parsing data: {e}")
        import traceback
        traceback.print_exc()
        
    return parsed_items

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
