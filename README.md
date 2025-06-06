# ⚡ Energy Insights Dashboard

Simulated analysis of regional energy usage across Australia, built to prep for a Data Analyst role at Tesla Energy APAC.

# 🎯 Project Overview
A full analytics pipeline:

- Synthetic data generation (Python).
- SQL transformations & analysis.
- Dashboards in Excel & Power BI.
- Temperature data from open-meteo.com.

# 🧠 Project Goals

- Practice advanced SQL (joins, window functions).
- Build dashboards for stakeholder insights.
- Mimic Tesla-style analytics workflows.
- Integrate external data sources (temperature data from open-meteo.com).

# 📊 Data Description
Simulated April-May 2025 energy usage across Melbourne, Sydney, Brisbane, and Perth.

|Column|Description|
|---|---|
|region|Geographic location (Melbourne, Sydney, Brisbane, Perth)|
|date|Date of data recording (April 2025 to May 2025)|
|kWh|Total energy consumed (in kWh)|
|devices|Number of active devices in region|
|uptime|Percent of time the system was online (%)|
|error_rate|Percent of operations that triggered errors (%)|
|temperature_2m_max|Maximum temperature in the region (°C), via open-meteo.com|

# 🌤️ Weather Data Integration
The project uses the Open-Meteo API to fetch daily maximum temperature data for all four cities. This data helps analyze how external temperatures correlate with energy usage.

Key Script: open_meteo.py

# 🛠️ Tools Used
- Python: Data generation (pandas, numpy, requests).
- SQL: Data transformation and analysis (SQLite).
- Microsoft Excel: Pivot tables, slicers, and initial dashboard.
- Power BI: Advanced interactive dashboard with slicers and KPI gauges.
- GitHub: Version control and project documentation.

# 📂 Project Structure
- /data – Generator script & CSV
- /db – SQLite DB & script
- /exports – SQL export outputs
- /dashboards/powerbi-dashboard.pbix – Power BI dashboard
- /dashboards/data_overview.xlsx – Excel dashboard

# 🚀 How to Use
- Run dataset_generator.py to create CSV
- Run open_meteo.py to get temperature data (from open-meteo.com)
- Use db_creator.py + SQL scripts to build DB & export results
- Open energy_dashboard.xlsx or energy_dashboard.pbix to explore dashboards

Note: Dashboards require manual refresh after data updates.

# 🔍 SQL Analysis Highlights
- Regional breakdowns of energy consumption.
- Device-normalized usage metrics (kWh per device).
- Top 5 energy usage days per region using window functions.
- Growth trends by region (first vs. last day).

# 📊 Power BI Dashboard
Built an interactive Power BI dashboard to analyze energy usage across Melbourne, Sydney, Brisbane, and Perth (April-May 2025).

![Default View](https://github.com/njanssen66/energy-insights-dashboard/blob/main/Default%20View.png?raw=true)
![Filtered View](https://github.com/njanssen66/energy-insights-dashboard/blob/main/Filtered%20View.png?raw=true)

# 🔄 Next Step: Power Automate
Automate CSV updates:

- Trigger: File change in OneDrive
- Action: Refresh Power BI
- Result: Always-current insights, no manual refresh needed