import requests
import pandas as pd
import numpy as np

def fetch_weather_data(city_coords: dict, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetch hourly solar radiation and temperature from Open-Meteo API for multiple cities and aggregate to daily.
    Parameters: city_coords (dict with city names and lat/lon), start_date, end_date (YYYY-MM-DD).
    Returns: DataFrame with region, date, avg solar radiation (W/m²), avg temperature (°C).
    """
    all_weather = []
    
    for city, coords in city_coords.items():
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": coords["latitude"],
            "longitude": coords["longitude"],
            "daily": "temperature_2m_max",
            "timezone": "Australia/Sydney",
            "start_date": start_date,
            "end_date": end_date,
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if "daily" not in data:
                raise ValueError(f"No hourly data for {city}")
            
            # Create DataFrame
            df = pd.DataFrame({
                "date": data["daily"]["time"],
                "temperature_2m_max": data["daily"]["temperature_2m_max"],
                "region": city
            })

            all_weather.append(df)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data for {city}: {e}")
    
    weather_df = pd.concat(all_weather, ignore_index=True) if all_weather else pd.DataFrame()
    if not weather_df.empty:
        print(f"Weather data shape: {weather_df.shape}")
        print(f"Weather data sample:\n{weather_df.head()}")

    return weather_df

def load_energy_data(file_path: str) -> pd.DataFrame:
    """
    Load energy usage data from CSV and clean it.
    Parameters: file_path (path to CSV file).
    Returns: DataFrame with region, date, kWh, and other columns.
    """
    try:
        df = pd.read_csv(file_path)
        # Ensure date is in YYYY-MM-DD string format
        df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
        # Handle missing values
        df = df.fillna({"kWh": df["kWh"].mean(), "devices": df["devices"].mean(),
                        "uptime": df["uptime"].mean(), "error_rate": df["error_rate"].mean()})
        print(f"Energy data shape: {df.shape}")
        print(f"Energy data sample:\n{df.head()}")
        return df
    except Exception as e:
        print(f"Error loading energy data: {e}")
        return pd.DataFrame()

def merge_and_analyze(energy_df: pd.DataFrame, weather_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merge energy and weather data, calculate correlations per city, and return combined DataFrame.
    Parameters: energy_df, weather_df (DataFrames with region and date columns).
    Returns: Merged DataFrame with correlation results printed.
    """
    if energy_df.empty or weather_df.empty:
        print("Empty DataFrame(s) detected. Cannot merge.")
        return pd.DataFrame()
    
    # Merge on region and date
    merged_df = pd.merge(energy_df, weather_df, on=["region", "date"], how="inner")
    print(f"Merged data shape: {merged_df.shape}")
    print(f"Merged data sample:\n{merged_df.head()}")
    
    # Calculate correlations per city
    if not merged_df.empty:
        for city in merged_df["region"].unique():
            city_df = merged_df[merged_df["region"] == city]
            if len(city_df) < 2:
                print(f"{city} - Too few data points ({len(city_df)}) for correlation.")
                continue
            # Check for sufficient variance
            if city_df["kWh"].std() == 0 or city_df["temperature_2m_max"].std() == 0:
                print(f"{city} - Insufficient variance in kWh, or temperature.")
                continue
            corr_temp = city_df["kWh"].corr(city_df["temperature_2m_max"])
            print(f"{city} - Correlation between kWh and temperature: {corr_temp:.3f}")
    
    return merged_df

def save_to_csv(df: pd.DataFrame, output_name: str):
    """Save DataFrame to CSV for Power BI integration."""
    output_path = f"{output_name}.csv"
    df.to_csv(output_path, index=False)
    print(f"Saved merged data to {output_path}")

if __name__ == "__main__":
    # Configuration
    city_coords = {
        "Melbourne": {"latitude": -37.8136, "longitude": 144.9631},
        "Sydney": {"latitude": -33.8688, "longitude": 151.2093},
        "Brisbane": {"latitude": -27.4698, "longitude": 153.0251},
        "Perth": {"latitude": -31.9505, "longitude": 115.8605}
    }
    start_date = "2025-03-18"
    end_date = "2025-05-27"
    energy_file = "energy_usage.csv"
    output_file = "energy_weather_apac"
    
    # Fetch weather data
    weather_df = fetch_weather_data(city_coords, start_date, end_date)
    
    # Load energy data
    energy_df = load_energy_data(energy_file)
    
    # Merge and analyze
    if not weather_df.empty and not energy_df.empty:
        merged_df = merge_and_analyze(energy_df, weather_df)
        if not merged_df.empty:
            save_to_csv(merged_df, output_file)