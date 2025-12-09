# Spec: Core Capabilities

## ADDED Requirements

### Requirement: Fetch Weather Data
The system MUST retrieve real-time weather data from the CWA API.

#### Scenario: Successful Fetch
-   Given a valid API Key and network connection
-   When the ETL process runs
-   Then it should receive a 200 OK response with valid JSON data containing weather observations.

### Requirement: Store Weather Data
The system MUST persist parsed weather data to a local SQLite database.

#### Scenario: Data Persistence
-   Given fetched weather data
-   When the data is processed
-   Then it should be inserted into the `weather_data` table in `data.db`.

### Requirement: Display Weather Table
The system MUST present the weather data in a user-friendly table format.

#### Scenario: View Table
-   Given the Streamlit app is running
-   When the user visits the main page
-   Then they should see a table listing cities and temperatures similar to the CWA website.
