import pandas as pd

INPUT_FILE = "Solar_photovoltaics_deployment_February_2026.xlsx"
INPUT_SHEET = "Table_3_dom_by_PC"

# Main output CSV - one row per constituency
OUTPUT_FILE = "solar_domestic_by_constituency.csv"


def derive_country(code):
    """
    Map ONS GSS constituency code to country using the first letter.
    E = England, W = Wales, S = Scotland, N = Northern Ireland.
    """
    if not isinstance(code, str) or len(code) == 0:
        return None
    return {
        "E": "England",
        "W": "Wales",
        "S": "Scotland",
        "N": "Northern Ireland",
    }.get(code[0])


# Read workbook - header row is the 4th row (0-indexed = 3)
df = pd.read_excel(INPUT_FILE, sheet_name=INPUT_SHEET, header=3)

# Rename to SQL-safe column names
df = df.rename(columns={
    "Constituency Code":        "constituency_code",
    "Country/Region":           "country_region",
    "Constituency":             "constituency_name",
    "Installed capacity (MW)":  "installed_capacity_mw",
    "Number of installations":  "number_of_installations",
})

# Filter to only actual constituency rows:
#   - constituency_name must be populated (aggregate rows have NaN here)
#   - exclude the top-of-sheet summary rows 'All constituencies' and 'Unallocated'
mask = (
    df["constituency_name"].notna()
    & (df["constituency_name"].astype(str).str.strip() != "")
    & (~df["constituency_name"].isin(["All constituencies", "Unallocated"]))
)
clean_df = df[mask].copy()

# Derive country column from the constituency code prefix
clean_df["country"] = clean_df["constituency_code"].apply(derive_country)

# Enforce data types
clean_df["installed_capacity_mw"] = pd.to_numeric(
    clean_df["installed_capacity_mw"], errors="coerce"
)
clean_df["number_of_installations"] = pd.to_numeric(
    clean_df["number_of_installations"], errors="coerce"
).astype("Int64")

# Reorder columns for readability
clean_df = clean_df[[
    "constituency_code",
    "constituency_name",
    "country",
    "country_region",
    "installed_capacity_mw",
    "number_of_installations",
]]

# Export
clean_df.to_csv(OUTPUT_FILE, index=False)

# Summary
print(f"Created: {OUTPUT_FILE}")
print(f"Rows: {len(clean_df)}")
print()
print("Country breakdown:")
print(clean_df["country"].value_counts().to_string())
print()
print(f"Total domestic capacity covered: {clean_df['installed_capacity_mw'].sum():,.1f} MW")
print(f"Total domestic installations covered: {clean_df['number_of_installations'].sum():,}")