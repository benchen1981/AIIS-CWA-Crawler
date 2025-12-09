# Proposal: Map Visualization

## Context
The user wants to visualize weather data on a map, similar to the CWA homepage. The current data granularity (Regional) is insufficient. We need city-level data (e.g., Taipei, Kaohsiung) with coordinates to render markers correctly.

## Requirements
-   **City-Level Data**: Fetch data for specific cities/counties (e.g., Keelung, Taipei, Taichung).
-   **Map Interface**: Display a map of Taiwan with markers.
-   **Dynamic Interaction**: Hovering or clicking markers should show temperature/weather details.
-   **Visuals**: Match CWA aesthetic (markers, varying colors based on temp if possible).

## Technical Changes
1.  **ETL Update**: Switch API from `F-A0010-001` (Regional Forecast) to `O-A0003-001` (Observation) or `F-C0032-001` (City Forecast) to get specific locations.
    *   *Decision*: Use `O-A0003-001` (Cowa Open Data - Real-time Observation) if available, as it provides specific station lat/lon.
2.  **Database**: Add `latitude` and `longitude` columns to `weather_data`.
3.  **UI**: Use `st.pydeck_chart` or `st.map` for visualization.
