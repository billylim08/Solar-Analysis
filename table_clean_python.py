import pandas as pd

file = "evci0101_2026-01_EV_chargers_by_region_and_country_UK.ods"

df = pd.read_excel(file, sheet_name="EVCI0101e", engine="odf", skiprows=2)

df.columns = [
    "date",
    "notes",
    "region_code",
    "region",
    "metric",
    "value"
]

df["date"] = pd.to_datetime(df["date"])
df["value"] = pd.to_numeric(df["value"], errors="coerce")

df.to_csv("uk_ev_chargers_clean.csv", index=False)