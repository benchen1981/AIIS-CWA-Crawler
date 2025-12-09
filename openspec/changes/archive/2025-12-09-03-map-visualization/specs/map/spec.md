# Spec: Map Visualization

## ADDED Requirements

### Requirement: Geographical Visualization
The app MUST display weather data on a geographical map of Taiwan.

#### Scenario: Map Display
-   Given the main page loaded
-   When the user views the "Map" section (or main view)
-   Then a map centered on Taiwan should be visible.
-   And markers should appear at weather station locations.

### Requirement: Data Granularity
The app MUST display data at the City/County level at minimum.

#### Scenario: Station Details
-   Given markers on the map
-   When the user interacts (hovers/clicks)
-   Then the specific city name and temperature should be displayed.
