# ⚡ Energy Insights Dashboard

A simulated data analysis project exploring regional energy usage trends across Australia, built as preparation for a Data Analyst role at Tesla Energy APAC (Req. ID 237346).

This project demonstrates a complete business analytics pipeline:

- Synthetic data generation using Python.
- SQL-based data transformation and advanced queries.
- Interactive visualizations and reporting using Excel and Power BI.

# 🧠 Project Goals
- Practice advanced SQL (joins, window functions, aggregates).
- Build interactive dashboards for stakeholder insights using Excel and Power BI.
- Simulate a real-world energy analytics workflow relevant to Tesla’s operations.

# 📊 Data Description
The dataset energy_usage.csv includes simulated energy usage metrics over time (Jan-Jun 2024) across four Australian regions: Melbourne, Sydney, Brisbane, and Perth.

|Column|Description|
|---|---|
|region|Geographic location (Melbourne, Sydney, Brisbane, Perth)|
|date|Date of data recording (Jan 2024 to Jun 2024)|
|kWh|Total energy consumed (in kWh)|
|devices|Number of active devices in region|
|uptime|Percent of time the system was online (%)|
|error_rate|Percent of operations that triggered errors (%)|

# 🛠️ Tools Used
- Python: Data generation (pandas, numpy).
- SQL: Data transformation and analysis (SQLite).
- Microsoft Excel: Pivot tables, slicers, and initial dashboard.
- Power BI: Advanced interactive dashboard with slicers and KPI gauges.
- GitHub: Version control and project documentation.

# 📂 Project Structure
- /data # Data generation script and CSV file
- /db # SQLite DB and creation script
- /exports # Automated CSV exports from SQL queries
- /powerbi-dashboard # Power BI dashboard file and screenshots
- energy_dashboard.xlsx # Excel dashboard file

# 🚀 How to Run
1. Generate Data:
 - Run data/dataset_generator.py to create the synthetic dataset energy_usage.csv.
2. Transform Data with SQL:
 - Use db/db_creator.py to create and populate the SQLite database.
 - Execute SQL queries from energy_queries.sql and export results using export_from_sql_file.py.
3. Visualize in Excel:
 - Open energy_dashboard.xlsx for interactive reporting with pivot tables and slicers.
4. Visualize in Power BI:
Open /powerbi-dashboard/energy_dashboard.pbix to explore the interactive Power BI dashboard.

# ⚠️ Important Note on Data Refresh
The Excel and Power BI dashboards do not automatically sync with the CSV exports. If you regenerate data or rerun SQL exports, manually refresh the data source in Excel or Power BI to reflect the latest information.

# 🔍 SQL Analysis Highlights
- Regional breakdowns of energy consumption.
- Device-normalized usage metrics (kWh per device).
- Top 5 energy usage days per region using window functions.
- Growth trends by region (first vs. last day).

# 📊 Power BI Dashboard
Built an interactive Power BI dashboard to analyze energy usage across Melbourne, Sydney, Brisbane, and Perth (Jan-Jun 2024).

Features:
- Time-series trends of energy usage by region.
- Total energy consumption (679K kWh).
- Average kWh per device and total consumption bar charts.
- Uptime (97.51%) and error rate (2.53%) gauges with targets (95% for uptime, 1% for error rate).
Interactivity:
- Region slicer (dropdown) to filter by Melbourne, Sydney, Brisbane, or Perth.
- Date range slicer to filter by time period.
Insights:
- Uptime consistently above the 95% target.
- Error rates below the 1% target.
- Melbourne has the highest energy usage (205K kWh) and kWh per device (35).

![Default View](https://github.com/njanssen66/energy-insights-dashboard/blob/main/Default%20View.png?raw=true)
![Filtered View](https://github.com/njanssen66/energy-insights-dashboard/blob/main/Filtered%20View.png?raw=true)

[Power BI File: energy_dashboard.pbix]