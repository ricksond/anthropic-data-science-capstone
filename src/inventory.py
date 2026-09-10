from pathlib import Path
import pandas as pd

DATA_DIR = Path('data')

FILES = [
    DATA_DIR / "aei_claude_ai_2026-06-26.csv",
    DATA_DIR / "aei_1p_api_2026-06-26.csv",
]


def inspect_file(file_path):
    print("\n" + "=" * 80)
    print(f"FILE: {file_path}")
    print("=" * 80)

    # File size
    size_mb = file_path.stat().st_size / (1024 ** 2)
    print(f"File size: {size_mb:.2f} MB")

    #Load Data

    df=pd.read_csv(file_path)

    #Basic Information
    print(f"\n Data Rows:{len(df)}.")
    print(f"\n Columns: {len(df.columns)}")

    # Columns and data types
    for col in df.columns:
        print(f"{col}:{df[col].dtype}")

    # Missing Values
    print(f"\n Missing Values Rates: ")
    missing=df.isna().sum() * 100

    for col, rate in  missing.items():
        print(f"{col}: {rate:.2f}%")

    # Date Range
    if "date_start" in df.columns and "date_end" in df.columns:
        print(" Date Range:")
        print(f"\n date_start: {df['date_start'].min()} → {df['date_start'].max()}")
        print(f"\n date_end:   {df['date_end'].min()} → {df['date_end'].max()}")

    # Geography
    if "geo_level" in df.columns:
        print("\nGeography levels:")
        print(df["geo_level"].value_counts().to_string())

     # Categories
    if "category_name" in df.columns:
        print("\nCategories:")
        print(df["category_name"].value_counts().to_string())

    # Metrics
    if "metric_id" in df.columns:
        print("\nMetrics:")
        print(df["metric_id"].value_counts().to_string())

    return df

def verify_targets(dataframes):
    print("\n" + "=" * 80)
    print("VERIFICATION TARGETS")
    print("=" * 80)

    claude = dataframes["aei_claude_ai_2026-06-26.csv"]
    api = dataframes["aei_1p_api_2026-06-26.csv"]

    # Date coverage
    for name, df in dataframes.items():
        dates = pd.to_datetime(df["date_start"])

        result = (
            dates.min() == pd.Timestamp("2026-04-01")
            and dates.max() == pd.Timestamp("2026-05-01")
        )

        print(f"{name} date range: {'PASS' if result else 'FAIL'}")

    # Claude geography levels
    expected_claude_geo = {"global", "country", "subregion"}
    actual_claude_geo = set(claude["geo_level"].unique())

    print(
        "Claude geography levels:",
        "PASS" if actual_claude_geo == expected_claude_geo else "FAIL"
    )

    # API geography
    expected_api_geo = {"global"}
    actual_api_geo = set(api["geo_level"].unique())

    print(
        "1P API geography levels:",
        "PASS" if actual_api_geo == expected_api_geo else "FAIL"
    )

    # Categories
    expected_categories = {
        "overall",
        "onet",
        "request",
        "soc_occupation",
    }

    for name, df in dataframes.items():
        actual_categories = set(df["category_name"].unique())

        print(
            f"{name} categories:",
            "PASS" if expected_categories.issubset(actual_categories) else "FAIL"
        )

    # Missing values
    for name, df in dataframes.items():
        has_missing = df.isna().any().any()

        print(
            f"{name} missing values:",
            "PASS" if not has_missing else "FAIL"
        )

def main():
    print("Anthropic Economic Index — Dataset Inventory")
    print("=" * 80)

    dataframes = {}

    for file_path in FILES:
        if not file_path.exists():
            print(f"\nERROR: File not found: {file_path}")
            continue

        dataframes[file_path.name] = inspect_file(file_path)

    if len(dataframes) == 2:
        verify_targets(dataframes)

    print("\n" + "=" * 80)
    print("Inventory complete.")
    print("=" * 80)


if __name__ == "__main__":
    main()