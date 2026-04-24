import pandas as pd

INPUT_FILE = "Solar_photovoltaics_deployment_February_2026.xlsx"
INPUT_SHEET = "Table_1_by_Capacity"

# Output CSV files
OUTPUT_GB = "solar_count_gb.csv"
OUTPUT_NI = "solar_count_ni.csv"
OUTPUT_UK = "solar_count_uk.csv"


def clean_date_label(x):
    """
    Convert labels like:
    Jan \n2010
    Feb 2026
    into pandas datetime objects
    """
    s = str(x).replace("\n", " ").replace("  ", " ").strip()
    return pd.to_datetime(s, format="%b %Y")


def clean_column_name(name):
    """
    Convert messy Excel labels into SQL-safe readable names
    """

    s = str(name).strip().lower()

    # Fix encoding issues
    s = s.replace("â‰¤", "<=")
    s = s.replace("≤", "<=")
    s = s.replace("≥", ">=")

    # Normalize spaces
    s = " ".join(s.split())

    mapping = {
        "0 to < 4 kw": "between_0_and_4_kw",
        "4 <= to < 10 kw": "between_4_and_10_kw",
        "10 <= to < 50 kw": "between_10_and_50_kw",
        "50 kw <= to < 5 mw": "between_50kw_and_5_mw",
        "5 <= to < 25 mw": "between_5_and_25_mw",
        ">= 25 mw": "greater_than_25_mw",
        "total": "total",
        "pre 2009 estimate [note 2]": "pre_2009_estimate",
        "of which: domestic [note 3]": "domestic"
    }

    return mapping.get(s, s.replace(" ", "_"))


def extract_region_block(df, region_name, start_row, end_row, date_row=32):
    """
    Extract one region block from cumulative count section
    """

    # Dates across top
    raw_dates = df.iloc[date_row, 1:]
    dates = [clean_date_label(x) for x in raw_dates]

    # Region rows
    block = df.iloc[start_row + 1:end_row, :].copy()

    # Categories
    categories = block.iloc[:, 0].astype(str).str.strip().tolist()
    clean_categories = [clean_column_name(c) for c in categories]

    # Values
    values = block.iloc[:, 1:].copy()
    values.columns = dates
    values.index = clean_categories
    values = values.apply(pd.to_numeric, errors="coerce")

    # Counts are whole numbers - use nullable Int64 so missing values stay NaN
    values = values.astype("Int64")

    # Transpose so dates are rows
    out = values.T.reset_index().rename(columns={"index": "date"})
    out.insert(0, "region", region_name)

    # SQL-safe date format
    out["date"] = pd.to_datetime(out["date"]).dt.strftime("%Y-%m-%d")

    return out


# Read workbook
df = pd.read_excel(INPUT_FILE, sheet_name=INPUT_SHEET, header=None)

# Extract data blocks
# CUMULATIVE COUNT section starts at row 32 (the date header row)
gb_df = extract_region_block(df, "GB", 33, 41)
ni_df = extract_region_block(df, "NI", 41, 49)
uk_df = extract_region_block(df, "UK", 49, 58)

# Export CSV files
gb_df.to_csv(OUTPUT_GB, index=False)
ni_df.to_csv(OUTPUT_NI, index=False)
uk_df.to_csv(OUTPUT_UK, index=False)

print("Created:")
print(OUTPUT_GB)
print(OUTPUT_NI)
print(OUTPUT_UK)