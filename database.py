import sqlite3
import os

# Use absolute path to ensure Streamlit finds the right DB
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, 'data.db')

def get_db_connection():
    # check_same_thread=False is needed for Streamlit's threading model
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    # Create table if not exists
    # Columns: id, city, town, temperature, obs_time
    c.execute('''
        CREATE TABLE IF NOT EXISTS weather_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            town TEXT NOT NULL,
            temperature REAL,
            obs_time TEXT,
            latitude REAL,
            longitude REAL
        )
    ''')
    conn.commit()
    conn.close()

def save_weather_data(data_list):
    """
    Saves a list of weather data dictionaries to the database.
    Each item in data_list should be a dict with keys: city, town, temperature, obs_time
    """
    conn = get_db_connection()
    c = conn.cursor()
    
    # Optional: Clear old data or handle duplicates depending on requirement.
    # For this iteration, we might want to clear table before inserting fresh batch
    # or just append. Let's clear to keep it simple as a "current state" snapshot.
    c.execute('DELETE FROM weather_data')
    
    c.executemany('''
        INSERT INTO weather_data (city, town, temperature, obs_time, latitude, longitude)
        VALUES (:city, :town, :temperature, :obs_time, :latitude, :longitude)
    ''', data_list)
    
    conn.commit()
    conn.close()

def get_weather_data():
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute('SELECT * FROM weather_data ORDER BY city, town')
        rows = c.fetchall()
        return [dict(row) for row in rows]
    except sqlite3.OperationalError as e:
        print(f"Database error: {e}")
        return []
    finally:
        conn.close()
