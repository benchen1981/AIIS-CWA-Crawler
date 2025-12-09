# Proposal: UI Refinements

## Context
The user has requested improvements to the UI:
1.  **Header Issue**: The header text "溫度分布圖 | 交通部中央氣象署" is obstructed.
2.  **Table Presentation**: The detailed list should be grouped by region (or city) using dropdowns/accordions, rather than a single long list.

## Requirements
-   **Fix Header**: Ensure the custom CSS header is visible and not overlapped by Streamlit elements or system bars.
-   **Grouped Data Display**: Use `st.expander` or grouping logic to organize the table. Since the data is currently mostly "City/Town", we can group by `City` (County).

## Implementation
1.  **CSS Update**: Adjust `z-index` or `padding` for the `.cwa-header` class.
2.  **Data Grouping**:
    -   Get unique `city` list.
    -   Loop through cities and create `st.expander(f"{city}")`.
    -   Inside each expander, show the dataframe filtered for that city (showing `town`, `temperature`, `obs_time`).
