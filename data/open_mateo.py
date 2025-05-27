import requests
import pandas as pd
import numpy as np

def fetch_weather_data(latitude: float, longitude: float, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetch hourly solar radiation and temperature from Open-Meteo API and aggregate to daily.
    Parameters: latitude, longitude (APAC city), start_date, end_date (YYYY-MM-DD).
    Returns: DataFrame with date, avg solar radiation (W/m²), avg temperature (°C).
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": "direct_radiation,temperature_2m",
        "timezone": "Australia/Melbourne"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "hourly" not in data:
            raise ValueError("No hourly data in API response")
        
        # Create DataFrame and aggregate to daily
        df = pd.DataFrame({
            "datetime": pd.to_datetime(data["hourly"]["time"]),
            "solar_radiation_wm2": data["hourly"]["direct_radiation"],
            "temperature_c": data["hourly"]["temperature_2m"]
        })
        
        # Convert datetime to date and group by date
        df["date"] = df["datetime"].dt.date
        daily_df = df.groupby("date").agg({
            "solar_radiation_wm2": "mean",
            "temperature_c": "mean"
        }).reset_index()
        
        # Convert date to string format (YYYY-MM-DD)
        daily_df["date"] = pd.to_datetime(daily_df["date"]).dt.strftime("%Y-%m-%d")
        return daily_df
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return pd.DataFrame()

def load_energy_data(file_path: str) -> pd.DataFrame:
    """
    Load energy usage data from CSV and clean it.
    Parameters: file_path (path to CSV file).
    Returns: DataFrame with date, kWh, and other columns.
    """
    try:
        df = pd.read_csv(file_path)
        # Ensure date is in YYYY-MM-DD string format
        df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
        # Handle missing values
        df = df.fillna({"kWh": df["kWh"].mean(), "devices": df["devices"].mean(),
                        "uptime": df["uptime"].mean(), "error_rate": df["error_rate"].mean()})
        return df
    except Exception as e:
        print(f"Error loading energy data: {e}")
        return pd.DataFrame()

def merge_and_analyze(energy_df: pd.DataFrame, weather_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merge energy and weather data, calculate correlations, and return combined DataFrame.
    Parameters: energy_df, weather_df (DataFrames with date column).
    Returns: Merged DataFrame with correlation results printed.
    """
    if energy_df.empty or weather_df.empty:
        return pd.DataFrame()
    
    # Merge on date
    merged_df = pd.merge(energy_df, weather_df, on="date", how="inner")
    
    # Calculate correlations
    if not merged_df.empty:
        corr_solar = merged_df["kWh"].corr(merged_df["solar_radiation_wm2"])
        corr_temp = merged_df["kWh"].corr(merged_df["temperature_c"])
        print(f"Correlation between kWh and solar radiation: {corr_solar:.3f}")
        print(f"Correlation between kWh and temperature: {corr_temp:.3f}")
    
    return merged_df

def save_to_csv(df: pd.DataFrame, city: str):
    """Save DataFrame to CSV for Power BI integration."""
    output_path = f"energy_weather_{city.replace(' ', '_').lower()}.csv"
    df.to_csv(output_path, index=False)
    print(f"Saved merged data to {output_path}")

if __name__ == "__main__":
    # Configuration
    melbourne_coords = {"latitude": -37.8136, "longitude": 144.9631}
    start_date = "2024-01-01"
    end_date = "2024-06-29"
    energy_file = "energy_usage.csv"
    
    # Fetch weather data
    weather_df = fetch_weather_data(
        melbourne_coords["latitude"],
        melbourne_coords["longitude"],
        start_date,
        end_date
    )
    
    # Load energy data
    energy_df = load_energy_data(energy_file)
    
    # Merge and analyze
    if not weather_df.empty and not energy_df.empty:
        merged_df = merge_and_analyze(energy_df, weather_df)
        if not merged_df.empty:
            save_to_csv(merged_df, "Melbourne")