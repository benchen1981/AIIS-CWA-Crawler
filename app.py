import streamlit as st
import pandas as pd
import pydeck as pdk
from database import get_weather_data
from etl import run_etl

# Page Config
st.set_page_config(page_title="溫度分布圖 | 交通部中央氣象署", layout="wide")

# Custom CSS to mimic CWA visual style
st.markdown("""
<style>
    /* Main Layout */
    .block-container {
        padding-top: 0rem;
    }
    
    /* CWA-like Header */
    .cwa-header {
        background-color: #1f3a93;
        color: white;
        padding: 15px 20px;
        font-size: 24px;
        font-weight: bold;
        font-family: 'PingFang TC', 'Microsoft JhengHei', 'Helvetica Neue', Helvetica, Arial, sans-serif;
        display: flex;
        align-items: center;
        margin-top: 80px;
        margin-bottom: 20px;
        z-index: 1000;
        position: relative;
        width: 100%;
    }
    
    /* Table Styling */
    .stTable {
        width: 100%;
        font-family: 'PingFang TC', 'Microsoft JhengHei', sans-serif;
    }
    thead tr th {
        background-color: #fce4ce !important;
        color: #333 !important;
        font-weight: bold !important;
        text-align: center !important;
        border-bottom: 2px solid #ddd !important;
    }
    tbody tr td {
        text-align: center !important;
        border-bottom: 1px solid #eee !important;
    }
    
    /* Button Styling */
    .stButton>button {
        background-color: #1f3a93;
        color: white;
        border-radius: 4px;
        padding: 5px 15px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #152b70;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Fake NavBar/Header
    st.markdown("""
        <div class="cwa-header">
            <span>溫度分布圖 | 交通部中央氣象署</span>
        </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns([6, 1])
    with cols[1]:
        if st.button("更新資料 (Refresh)"):
            with st.spinner('Downloading and Processing data...'):
                status = run_etl()
            if status == "Success":
                st.success('Data updated!')
                st.rerun()
            else:
                st.error(f"Update failed: {status}")

    data = get_weather_data()
    
    if not data:
        with st.spinner('Initial data fetch...'):
            status = run_etl()
            if status == "Success":
                data = get_weather_data()
            else:
                st.error(f"Automatic data fetch failed: {status}")
    
    if not data:
        st.warning("目前無資料，請點擊「更新資料」。")
    else:
        df = pd.DataFrame(data)
        
        if not df.empty:
            # === Map Visualization ===
            st.subheader("臺灣氣溫分布圖")
            
            # ... Color and Map logic remains same ...
            def get_color(temp):
                if temp is None: return [200, 200, 200, 200]
                if temp < 10: return [0, 0, 255, 200]
                elif temp < 20: return [0, 255, 255, 200]
                elif temp < 25: return [0, 255, 0, 200]
                elif temp < 30: return [255, 165, 0, 200]
                else: return [255, 0, 0, 200]

            df['color'] = df['temperature'].apply(get_color)
            
            layer = pdk.Layer(
                "ScatterplotLayer",
                data=df,
                get_position=["longitude", "latitude"],
                get_color="color",
                get_radius=5000, # Adjusted radius
                pickable=True,
                opacity=0.8,
                stroked=True,
                filled=True,
                radius_scale=1,
                radius_min_pixels=3,
                radius_max_pixels=30,
            )

            view_state = pdk.ViewState(
                latitude=23.7,
                longitude=121.0,
                zoom=6.5,
                pitch=0
            )

            # Ensure coordinates are numeric
            df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
            df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
            df = df.dropna(subset=['latitude', 'longitude'])

            st.pydeck_chart(pdk.Deck(
                map_style=None, # Use default style to avoid token issues
                initial_view_state=view_state,
                layers=[layer],
                tooltip={
                    "html": "<b>{city} {town}</b><br/>溫度: {temperature}°C<br/>時間: {obs_time}",
                    "style": {
                        "backgroundColor": "steelblue",
                        "color": "white"
                    }
                }
            ))
            
            # === Table Grouped by City ===
            st.subheader("詳細資料列表 (依縣市分組)")
            
            # Sort by City then Town
            df = df.sort_values(by=['city', 'town'])
            
            # Get unique cities
            unique_cities = df['city'].unique()
            
            # Create Expanders for each city
            for city in unique_cities:
                with st.expander(f"{city}"):
                    city_df = df[df['city'] == city]
                    display_df = city_df[['town', 'temperature', 'obs_time']]
                    display_df.columns = ['地點', '溫度 (°C)', '觀測時間']
                    st.table(display_df)
        else:
            st.info("資料庫為空。")

if __name__ == "__main__":
    main()
