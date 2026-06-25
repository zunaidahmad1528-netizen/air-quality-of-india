"""
India Air Quality EDA — src/eda_analysis.py
Generates all figures saved to outputs/figures/
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from scipy import stats
import warnings
import os

warnings.filterwarnings("ignore")

# ── Paths ────────────────────────────────────────────────────────────────────
BASE   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA   = os.path.join(BASE, "data",    "india_air_quality_2019_2023.csv")
OUTDIR = os.path.join(BASE, "outputs", "figures")
os.makedirs(OUTDIR, exist_ok=True)

# ── Style ────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor":  "white",
    "axes.facecolor":    "#F8F8F8",
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.grid":         True,
    "grid.color":        "white",
    "grid.linewidth":    1.0,
    "font.family":       "sans-serif",
    "font.size":         11,
    "axes.titlesize":    13,
    "axes.titleweight":  "bold",
    "axes.labelsize":    11,
    "xtick.labelsize":   10,
    "ytick.labelsize":   10,
})

PALETTE   = ["#E63946", "#457B9D", "#2A9D8F", "#E9C46A", "#F4A261",
             "#264653", "#6D6875", "#B5838D", "#A8DADC", "#1D3557"]
CITY_CLR  = dict(zip(
    ["Delhi","Mumbai","Bengaluru","Kolkata","Chennai",
     "Hyderabad","Ahmedabad","Pune","Lucknow","Jaipur"],
    PALETTE
))

def save(name):
    path = os.path.join(OUTDIR, name)
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {name}")

# ── Load & clean ─────────────────────────────────────────────────────────────
df = pd.read_csv(DATA)

print("=== 1. Dataset Overview ===")
print(f"Shape       : {df.shape}")
print(f"Missing vals:\n{df.isnull().sum()}\n")

# Impute missing PM values with city-month median
for col in ["pm2_5", "pm10"]:
    df[col] = df.groupby(["city","month"])[col].transform(
        lambda x: x.fillna(x.median())
    )
print("Missing after imputation:", df.isnull().sum().sum())

# AQI category
def aqi_category(val):
    if val <= 50:   return "Good"
    if val <= 100:  return "Satisfactory"
    if val <= 200:  return "Moderate"
    if val <= 300:  return "Poor"
    if val <= 400:  return "Very Poor"
    return "Severe"

df["aqi_category"] = df["aqi"].apply(aqi_category)
df["season"] = df["month"].map({
    12:"Winter",1:"Winter",2:"Winter",
    3:"Spring",4:"Spring",5:"Spring",
    6:"Monsoon",7:"Monsoon",8:"Monsoon",9:"Monsoon",
    10:"Post-Monsoon",11:"Post-Monsoon"
})

# ── Fig 1 — AQI heatmap (city × month) ──────────────────────────────────────
print("\n=== Fig 1: AQI Heatmap ===")
pivot = df.groupby(["city","month"])["aqi"].mean().unstack()
month_labels = ["Jan","Feb","Mar","Apr","May","Jun",
                "Jul","Aug","Sep","Oct","Nov","Dec"]
pivot.columns = month_labels

fig, ax = plt.subplots(figsize=(13, 6))
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="RdYlGn_r",
            linewidths=0.4, ax=ax,
            cbar_kws={"label": "Mean AQI", "shrink": 0.8})
ax.set_title("Average AQI by City and Month (2019 – 2023)")
ax.set_xlabel("")
ax.set_ylabel("")
plt.tight_layout()
save("01_aqi_heatmap_city_month.png")

# ── Fig 2 — Annual AQI trend per city ───────────────────────────────────────
print("=== Fig 2: Annual AQI Trend ===")
annual = df.groupby(["year","city"])["aqi"].mean().reset_index()

fig, ax = plt.subplots(figsize=(11, 6))
for city, grp in annual.groupby("city"):
    ax.plot(grp["year"], grp["aqi"], marker="o", linewidth=2,
            color=CITY_CLR[city], label=city)
ax.set_title("Annual Mean AQI Trend by City")
ax.set_xlabel("Year")
ax.set_ylabel("Mean AQI")
ax.legend(loc="upper right", fontsize=9, ncol=2, framealpha=0.5)
ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
plt.tight_layout()
save("02_annual_aqi_trend.png")

# ── Fig 3 — COVID lockdown effect (Delhi PM2.5) ──────────────────────────────
print("=== Fig 3: COVID Lockdown Effect ===")
delhi = df[df["city"] == "Delhi"].copy()
delhi["date"] = pd.to_datetime(
    delhi["year"].astype(str) + "-" + delhi["month"].astype(str).str.zfill(2) + "-01"
)
delhi = delhi.sort_values("date")

fig, ax = plt.subplots(figsize=(13, 5))
ax.fill_between(delhi["date"], delhi["pm2_5"], alpha=0.15, color="#E63946")
ax.plot(delhi["date"], delhi["pm2_5"], color="#E63946", linewidth=1.8)
ax.axvspan(pd.Timestamp("2020-04-01"), pd.Timestamp("2020-06-30"),
           alpha=0.15, color="#2A9D8F", label="Lockdown period (Apr–Jun 2020)")
ax.axhline(60, linestyle="--", color="#264653", linewidth=1.2,
           label="WHO 24-hr guideline (60 µg/m³)")
ax.set_title("Delhi PM2.5 Monthly Trend — COVID Lockdown Impact")
ax.set_xlabel("Date")
ax.set_ylabel("PM2.5 (µg/m³)")
ax.legend(fontsize=9)
plt.tight_layout()
save("03_delhi_covid_lockdown_pm25.png")

# ── Fig 4 — Seasonal boxplot (PM2.5 across cities) ──────────────────────────
print("=== Fig 4: Seasonal PM2.5 Distribution ===")
season_order = ["Winter","Spring","Monsoon","Post-Monsoon"]

fig, ax = plt.subplots(figsize=(11, 6))
sns.boxplot(data=df, x="season", y="pm2_5", order=season_order,
            palette=["#457B9D","#2A9D8F","#E9C46A","#F4A261"],
            width=0.5, linewidth=1.2, flierprops=dict(marker=".", alpha=0.4), ax=ax)
ax.set_title("PM2.5 Distribution by Season (All Cities, 2019–2023)")
ax.set_xlabel("Season")
ax.set_ylabel("PM2.5 (µg/m³)")
plt.tight_layout()
save("04_seasonal_pm25_boxplot.png")

# ── Fig 5 — Correlation heatmap ──────────────────────────────────────────────
print("=== Fig 5: Correlation Heatmap ===")
corr_cols = ["pm2_5","pm10","no2","so2","co","aqi"]
corr = df[corr_cols].corr()

fig, ax = plt.subplots(figsize=(7, 6))
mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm",
            center=0, linewidths=0.4, ax=ax,
            cbar_kws={"shrink": 0.8})
ax.set_title("Pollutant Correlation Matrix")
plt.tight_layout()
save("05_pollutant_correlation.png")

# ── Fig 6 — City ranking (mean AQI 2019–2023) ───────────────────────────────
print("=== Fig 6: City AQI Ranking ===")
ranking = df.groupby("city")["aqi"].mean().sort_values(ascending=True)
colors   = [CITY_CLR[c] for c in ranking.index]

fig, ax = plt.subplots(figsize=(9, 6))
bars = ax.barh(ranking.index, ranking.values, color=colors, height=0.6)
for bar, val in zip(bars, ranking.values):
    ax.text(val + 1, bar.get_y() + bar.get_height()/2,
            f"{val:.0f}", va="center", fontsize=10)
ax.set_title("City Ranking by Mean AQI (2019 – 2023)")
ax.set_xlabel("Mean AQI")
ax.set_xlim(0, ranking.max() * 1.15)
plt.tight_layout()
save("06_city_aqi_ranking.png")

# ── Fig 7 — AQI category distribution (stacked bar per city) ────────────────
print("=== Fig 7: AQI Category Distribution ===")
cat_order = ["Good","Satisfactory","Moderate","Poor","Very Poor","Severe"]
cat_colors = {"Good":"#2A9D8F","Satisfactory":"#57CC99","Moderate":"#E9C46A",
              "Poor":"#F4A261","Very Poor":"#E76F51","Severe":"#E63946"}

city_cat = (df.groupby(["city","aqi_category"])
              .size().unstack(fill_value=0)
              .reindex(columns=cat_order, fill_value=0))
city_cat_pct = city_cat.div(city_cat.sum(axis=1), axis=0) * 100

fig, ax = plt.subplots(figsize=(13, 6))
bottom = np.zeros(len(city_cat_pct))
for cat in cat_order:
    vals = city_cat_pct[cat].values
    ax.bar(city_cat_pct.index, vals, bottom=bottom,
           label=cat, color=cat_colors[cat], width=0.6)
    bottom += vals

ax.set_title("AQI Category Distribution by City (% of Months)")
ax.set_xlabel("")
ax.set_ylabel("Percentage of months (%)")
ax.legend(loc="upper right", fontsize=9, ncol=3)
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
save("07_aqi_category_distribution.png")

# ── Fig 8 — Statistical summary table ───────────────────────────────────────
print("=== Fig 8: Statistical Summary ===")
stats_df = df.groupby("city")[["pm2_5","pm10","aqi"]].agg(["mean","median","std"])
stats_df.columns = ["PM2.5 Mean","PM2.5 Med","PM2.5 SD",
                    "PM10 Mean","PM10 Med","PM10 SD",
                    "AQI Mean","AQI Med","AQI SD"]
stats_df = stats_df.round(1).sort_values("AQI Mean", ascending=False)

fig, ax = plt.subplots(figsize=(14, 4))
ax.axis("off")
tbl = ax.table(
    cellText=stats_df.values,
    rowLabels=stats_df.index,
    colLabels=stats_df.columns,
    cellLoc="center", loc="center"
)
tbl.auto_set_font_size(False)
tbl.set_fontsize(9)
tbl.scale(1, 1.5)
for (r, c), cell in tbl.get_celld().items():
    if r == 0 or c == -1:
        cell.set_facecolor("#264653")
        cell.set_text_props(color="white", fontweight="bold")
    elif r % 2 == 0:
        cell.set_facecolor("#F0F4F8")
ax.set_title("Descriptive Statistics by City", fontsize=13, fontweight="bold", pad=20)
plt.tight_layout()
save("08_descriptive_stats_table.png")

print("\nAll figures saved to outputs/figures/")
