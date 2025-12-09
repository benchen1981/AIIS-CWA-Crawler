# Project Context

## Purpose
Develop a Python-based application to fetch, store, and display weather data from the Central Weather Administration (CWA). The system will download JSON data, parse it, store it in a local SQLite database, and present it via a Streamlit web interface mimicking the official CWA temperature page.

## Tech Stack
-   **Language**: Python 3
-   **Web Framework**: Streamlit
-   **Database**: SQLite (`data.db`)
-   **Data Source**: CWA Open Data API (JSON format)
-   **Libraries**: `requests` (API), `pandas` (Data Processing), `sqlite3` (Database)

## Project Conventions

### Code Style
-   Follow PEP 8 guidelines for Python code.
-   Use descriptive variable and function names.
-   Include docstrings for functions and modules.

### Architecture Patterns
-   **ETL Pipeline**: Extract (API), Transform (Parse/Clean), Load (SQLite).
-   **UI Layer**: Streamlit app reading directly from the database to display data.

### Testing Strategy
-   Unit tests for data parsing and database operations.
-   Manual verification of the UI against the CWA reference page.

## Domain Context
-   **Source**: [CWA Observation Data](https://www.cwa.gov.tw/V8/C/W/OBS_Temp.html)
-   **Dataset**: F-A0010-001 (Forecast/Observation data)
-   **API Key**: Provided in constraints.

## Important Constraints
-   API Key: `CWA-1FFDDAEC-161F-46A3-BE71-93C32C52829F` (or `CWA-6FAB2E54-79BE-438F-8453-B059902602DC` for specific file download).
-   Must use SQLite for storage.
-   Must replicate the specific Web UI layout where possible.

