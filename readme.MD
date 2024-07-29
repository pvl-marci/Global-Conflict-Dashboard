# Global Conflicts Data Dashboard

![Dashboard Screenshot](screenshots\dashboard.png)

This repository contains an interactive dashboard for visualizing global conflict data, developed as part of a Bachelor Thesis in 2022. The dashboard is built with Plotly Dash in Python and provides insights into worldwide conflicts, their types, and their correlation with economic indicators and Google Trends.

## Project Description

The Global Conflicts Data Dashboard offers a comprehensive visualization of conflict data across the globe. It includes various interactive elements to explore the types of conflicts, their distribution over the years, and their relationship with economic indicators in G8+5 countries.

## Features

- **Worldwide Conflicts Visualization**: Interactive map showing the distribution and types of conflicts over the years.
- **Conflict Type vs. Economy**: Comparative analysis of conflict types against GDP growth in G8+5 countries.
- **Google Trends Analysis**: Insights into Google search trends related to various conflict types over time.
- **Interactive Filters**: Dynamic selection of countries, KPIs and conflict types for tailored visualizations.

## Setup Instructions

To run this dashboard locally, follow these steps:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/global-conflicts-dashboard.git
   cd global-conflicts-dashboard
   ```

2. **Create and Activate Virtual Environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Dashboard**:

   ```bash
   python app.py
   ```

5. **Open in Browser**:
   Open your web browser and navigate to `http://127.0.0.1:8050/` to view the dashboard.

## Usage

Once the dashboard is running, you can use various interactive features to explore the data:

- **Conflict Map**: Use the timeline slider to view conflicts over different years and select conflict types to filter the data on the map.
- **GDP vs. Conflict Analysis**: Select a country and economic indicator to compare with conflict data over time.
- **Google Trends**: Toggle between different conflict types to see how often they were searched on Google over the weeks.

## Data Sources

The data used in this dashboard is sourced from:

- [The Uppsala Conflict Data Program (UCDP)](https://ucdp.uu.se/)
- [World Bank Open Data](https://data.worldbank.org/)
- [Google Trends](https://trends.google.com/trends/)
- [HIIK](https://hiik.de/)

## Contributions

Contributions are welcome! If you have any ideas or improvements, feel free to open an issue or submit a pull request.

## Acknowledgements

This dashboard was developed as part of a Bachelor Thesis in 2022. Special thanks to the advisors and contributors who provided guidance and support throughout the project.
