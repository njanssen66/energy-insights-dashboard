import pandas as pd
import sqlite3

# Load CSV
df = pd.read_csv("../data/energy_weather_apac.csv")

# Connect to SQLite
conn = sqlite3.connect("energy_usage.db")

# Write to database
df.to_sql("energy_usage", conn, if_exists="replace", index=False)

conn.close()
