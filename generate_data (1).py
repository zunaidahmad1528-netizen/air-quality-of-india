import pandas as pd
import numpy as np

np.random.seed(42)

cities = {
    "Delhi":      {"pm25_base": 120, "pm10_base": 210, "aqi_base": 180},
    "Mumbai":     {"pm25_base": 65,  "pm10_base": 110, "aqi_base": 105},
    "Bengaluru":  {"pm25_base": 45,  "pm10_base": 80,  "aqi_base": 75},
    "Kolkata":    {"pm25_base": 90,  "pm10_base": 155, "aqi_base": 145},
    "Chennai":    {"pm25_base": 50,  "pm10_base": 88,  "aqi_base": 82},
    "Hyderabad":  {"pm25_base": 55,  "pm10_base": 95,  "aqi_base": 90},
    "Ahmedabad":  {"pm25_base": 75,  "pm10_base": 130, "aqi_base": 120},
    "Pune":       {"pm25_base": 48,  "pm10_base": 84,  "aqi_base": 78},
    "Lucknow":    {"pm25_base": 100, "pm10_base": 175, "aqi_base": 160},
    "Jaipur":     {"pm25_base": 85,  "pm10_base": 148, "aqi_base": 135},
}

seasons = {
    1: 1.6, 2: 1.4, 3: 1.0, 4: 0.85, 5: 0.75, 6: 0.65,
    7: 0.55, 8: 0.55, 9: 0.70, 10: 1.1, 11: 1.5, 12: 1.7
}

years = [2019, 2020, 2021, 2022, 2023]
records = []

for year in years:
    for month in range(1, 13):
        for city, params in cities.items():
            seasonal_factor = seasons[month]
            covid_factor = 0.65 if (year == 2020 and month in [4, 5, 6]) else 1.0
            trend_factor = 1 - (year - 2019) * 0.03

            pm25 = round(params["pm25_base"] * seasonal_factor * covid_factor * trend_factor
                         + np.random.normal(0, 8), 1)
            pm10 = round(params["pm10_base"] * seasonal_factor * covid_factor * trend_factor
                         + np.random.normal(0, 12), 1)
            no2  = round(np.random.normal(45, 15) * seasonal_factor * covid_factor, 1)
            so2  = round(np.random.normal(18, 6)  * seasonal_factor * covid_factor, 1)
            co   = round(np.random.normal(1.2, 0.4) * seasonal_factor * covid_factor, 2)
            aqi  = round(params["aqi_base"] * seasonal_factor * covid_factor * trend_factor
                         + np.random.normal(0, 15), 0)

            pm25 = max(pm25, 5.0)
            pm10 = max(pm10, 10.0)
            aqi  = max(aqi, 20.0)

            # Inject ~3% missing values
            if np.random.rand() < 0.03:
                pm25 = np.nan
            if np.random.rand() < 0.03:
                pm10 = np.nan

            records.append({
                "year": year, "month": month, "city": city,
                "pm2_5": pm25, "pm10": pm10, "no2": no2,
                "so2": so2, "co": co, "aqi": aqi,
                "station_count": np.random.randint(3, 12)
            })

df = pd.DataFrame(records)
df.to_csv("india_air_quality_2019_2023.csv", index=False)
print(f"Dataset saved: {len(df)} rows, {df.shape[1]} columns")
print(df.head())
