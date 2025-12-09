# Proposal: CWA Weather App

## Context
The goal is to build a Python application that fetches weather data from the Central Weather Administration (CWA), processes it, stores it in an SQLite database, and displays it via a Streamlit web interface. This app will replicate the functionality and look of the CWA temperature observation page.

## Requirements
-   **Fetch Data**: Use the CWA Open Data API (F-A0010-001) to get weather data.
-   **Storage**: Parse and store the data in a `data.db` SQLite database.
-   **UI**: Create a Streamlit app to display the data, mimicking the CWA website table.
-   **Environment**: Python environment with `requests`, `pandas`, `streamlit`.

## Out of Scope
-   Automated scheduling (e.g., cron jobs) for this iteration (manual run or load on start).
-   User authentication (Single user/Open access).
-   Deployment to cloud (Localhost only).
