import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
random.seed(42)
np.random.seed(42)

regions = ['Melbourne', 'Sydney', 'Brisbane', 'Perth']
start_date = datetime.strptime('2025-03-18', '%Y-%m-%d')
end_date = start_date + timedelta(days=180)  # ~6 months of data
dates = pd.date_range(start=start_date, end=end_date)

# Generate synthetic data
data = []
for region in regions:
    base_kWh = random.randint(800, 1300)
    base_devices = random.randint(30, 50)
    for date in dates:
        kWh = base_kWh + np.random.normal(0, 50)
        devices = base_devices + np.random.randint(-3, 4)
        uptime = round(np.random.uniform(95, 100), 2)  # percentage
        error_rate = round(np.random.uniform(0, 5), 2)  # percentage
        data.append([region, date.date(), round(kWh), devices, uptime, error_rate])

# Create DataFrame
df = pd.DataFrame(data, columns=['region', 'date', 'kWh', 'devices', 'uptime', 'error_rate'])
df.head()

output_file_path = 'energy_usage.csv'

# Save the DataFrame to a CSV file
df.to_csv(output_file_path, index=False)

print(f"Data saved to: {output_file_path}")