# CWA Weather App (AIIS-CWA-Crawler)

A Python-based web application that crawls, stores, and visualizes real-time weather data from the [Central Weather Administration (CWA)](https://www.cwa.gov.tw/) of Taiwan. Built with **Streamlit** and **PyDeck**, this app provides an interactive map and detailed observation data mimicking the visual style of the official CWA website.

🌟[App Screenshot](https://github.com/benchen1981/AIIS-CWA-Crawler/assets/placeholder.png)
*(Note: You can update this screenshot link after uploading images to your repo)*

# =================================================================
## Prompt Task to Agent :
中央氣象局(CWA) HTML 版溫度 資料爬蟲
中央氣象局 : https://www.cwa.gov.tw/V8/C/W/OBS_Temp.html
CWA 登入頁 : https://opendata.cwa.gov.tw/userLogin
 API 金鑰: CWA-1FFDDAEC-161F-46A3-BE71-93C32C52829F
教學使用的 JSON Dataset（F-A0010-001）
網站資料頁：
https://opendata.cwa.gov.tw/dataset/forecast/F-A0010-001
JSON 下載網址 : https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-A0010-001?Authorization=CWA-6FAB2E54-79BE-438F-8453-B059902602DC&downloadType=WEB&format=JSON
要求(Part 1)
1. 使用 Python 建立
2. 使用API 下載中央氣象局 F-A0010-001 JSON 資料
3. 解析資料：取出各地區的溫度
4. 設計 SQLite 資料庫(data.db)，資料庫名稱：data.db，資料表：依原始資料排序及優化，把解析後的資料「存進 SQLite3」
5. Streamlit App，並顯示從 SQLite 讀出的資料表格。
6. Web UI 參照 : https://www.cwa.gov.tw/V8/C/W/OBS_Temp.html
# =================================================================


## 🌟 Features

*   **Real-time Data ETL**: Fetches the latest live observation data (`O-A0003-001`) from CWA Open Data API.
*   **Local Storage**: Parses and stores weather data (Temperature, Date, Location) in a local `SQLite` database.
*   **Interactive Map**: Visualizes weather stations across Taiwan using `PyDeck`.
    *   Markers colored by temperature intensity (Cool to Hot).
    *   Tooltips displaying Station Name, Temperature, and Observation Time.
*   **CWA-Styled UI**: A polished interface inspired by the CWA official site, featuring:
    *   Official blue color scheme and headers.
    *   Responsive layout with clean typography (supporting Traditional Chinese).
*   **Grouped Data Display**: Detailed weather data is grouped by City/County in expandable sections for easy navigation.

## 🛠️ Technology Stack

*   **Language**: Python 3.10+
*   **Web Framework**: [Streamlit](https://streamlit.io/)
*   **Visualization**: [PyDeck](https://pydeck.gl/) (Deck.gl wrapper)
*   **Database**: SQLite
*   **Data Source**: CWA Open Data API (JSON)

## 🚀 Getting Started

### Prerequisites

*   Python 3 installed.
*   An API Key from [CWA Open Data](https://opendata.cwa.gov.tw/). (Currently hardcoded for demo purposes, but customizable in `etl.py`).

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/benchen1981/AIIS-CWA-Crawler.git
    cd AIIS-CWA-Crawler
    ```

2.  Install required packages:
    ```bash
    pip install streamlit pandas requests pydeck
    ```

3.  (Optional) Initialize the database and fetch data manually:
    ```bash
    python etl.py
    ```

### Running the App

Start the Streamlit server:

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

## 📂 Project Structure

*   `app.py`: Main Streamlit application entry point. Handles UI rendering and map visualization.
*   `etl.py`: ETL (Extract, Transform, Load) script. Fetches JSON data from CWA, parses it, and saves it to SQLite.
*   `database.py`: Database management module. Handles connection and schema (SQLite).
*   `openspec/`: Project specifications and change management logs (OpenSpec).

## 📊 Data Source

This application uses the **Automatic Weather Station (AWS)** dataset (`O-A0003-001`) from the Central Weather Administration, Taiwan.

## 📝 License

This project is created for educational purposes (Lecture 14 Practice).
