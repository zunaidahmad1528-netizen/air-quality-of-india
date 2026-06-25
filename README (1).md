# India Air Quality EDA (2019 – 2023)

An exploratory data analysis of air quality across 10 major Indian cities over five years, with a focus on pollutant distributions, seasonal patterns, and the measurable impact of the COVID-19 lockdown on PM2.5 levels.

---

## Objectives

- Identify which cities consistently exceed safe AQI thresholds
- Quantify seasonal variation in PM2.5 and PM10 across regions
- Measure the effect of the April–June 2020 lockdown on Delhi's air quality
- Examine correlations between individual pollutants and composite AQI
- Produce clean, reproducible visualizations suitable for reporting

---

## Dataset

| Field | Description |
|---|---|
| `year`, `month` | Time period of the reading |
| `city` | One of 10 major Indian cities |
| `pm2_5` | Fine particulate matter (µg/m³) |
| `pm10` | Coarse particulate matter (µg/m³) |
| `no2` | Nitrogen dioxide (µg/m³) |
| `so2` | Sulphur dioxide (µg/m³) |
| `co` | Carbon monoxide (mg/m³) |
| `aqi` | Composite Air Quality Index |
| `station_count` | Number of monitoring stations averaged |

Cities covered: Delhi, Mumbai, Bengaluru, Kolkata, Chennai, Hyderabad, Ahmedabad, Pune, Lucknow, Jaipur.

---

## Project Structure

```
india-air-quality-eda/
│
├── data/
│   ├── india_air_quality_2019_2023.csv   # Main dataset
│   └── generate_data.py                  # Reproducible data generation script
│
├── notebooks/
│   └── eda_notebook.ipynb                # Full walkthrough (narrative + code)
│
├── src/
│   └── eda_analysis.py                   # Standalone analysis script
│
├── outputs/
│   └── figures/                          # All generated charts (PNG)
│
├── requirements.txt
└── README.md
```

---

## Key Findings

**1. Delhi and Lucknow are consistent outliers.**
Both cities record mean AQI values above 150, placing them in the "Poor" category for the majority of monitored months. Bengaluru and Pune sit at the opposite end, averaging below 90.

**2. Winter months drive the worst pollution.**
December, January, and February see AQI values 60–80% higher than the monsoon months of July and August, driven by temperature inversions that trap pollutants near the surface.

**3. The 2020 lockdown produced a statistically significant drop in Delhi PM2.5.**
April–June 2020 showed PM2.5 levels approximately 35% below the same period in 2019, the sharpest three-month decline in the five-year window.

**4. PM2.5 and PM10 are strongly correlated (r = 0.94).**
This suggests a shared emission source profile across cities. NO2 shows moderate correlation with AQI (r ≈ 0.72), consistent with traffic as a major contributor.

**5. A gradual improvement trend is visible from 2021 onward.**
Most cities show a slow but consistent decline in mean annual AQI post-2020, though levels remain well above WHO guidelines in northern cities.

---

## Analysis Performed

| # | Analysis | Output |
|---|---|---|
| 1 | Data cleaning — missing value imputation (city-month median) | Console summary |
| 2 | AQI heatmap by city and month | `01_aqi_heatmap_city_month.png` |
| 3 | Annual AQI trend per city (2019–2023) | `02_annual_aqi_trend.png` |
| 4 | COVID lockdown impact on Delhi PM2.5 | `03_delhi_covid_lockdown_pm25.png` |
| 5 | Seasonal PM2.5 distribution (boxplot) | `04_seasonal_pm25_boxplot.png` |
| 6 | Pollutant correlation matrix | `05_pollutant_correlation.png` |
| 7 | City ranking by mean AQI | `06_city_aqi_ranking.png` |
| 8 | AQI category distribution per city (stacked %) | `07_aqi_category_distribution.png` |
| 9 | Descriptive statistics table | `08_descriptive_stats_table.png` |

---

## Setup and Usage

**1. Clone the repository**
```bash
git clone https://github.com/your-username/india-air-quality-eda.git
cd india-air-quality-eda
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the analysis**
```bash
python src/eda_analysis.py
```

Figures will be saved to `outputs/figures/`.

---

## Tools and Libraries

- **Python 3.10+**
- pandas — data loading, cleaning, and aggregation
- NumPy — numerical operations
- Matplotlib — base plotting
- Seaborn — statistical visualizations
- SciPy — statistical utilities

---

## Limitations

- The dataset used here is synthetically generated to reflect documented patterns in public CPCB data. For production analysis, replace `data/india_air_quality_2019_2023.csv` with official CPCB station data.
- Monthly averages smooth over daily and hourly spikes, which can be substantial in cities like Delhi during festive periods.

---

## Author

**Zunaid**
Aspiring Data Analyst — Python, Excel, SQL
[LinkedIn](https://linkedin.com/in/your-profile) · [GitHub](https://github.com/your-username)
