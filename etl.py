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
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

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
    # NOTE: We are NOT calling init_db() here to force wipe every time, 
    # but database.py's save_weather_data now clears the table.
    # Ensure DB exists first.
    init_db() 
    
    data = fetch_data()
    if not data:
        print("No data fetched.")
        return
    parsed = parse_data(data)
    print(f"Parsed {len(parsed)} records.")
    if parsed:
        save_weather_data(parsed)
        print("Data saved to database.")
    print("ETL completed.")

if __name__ == "__main__":
    run_etl()
