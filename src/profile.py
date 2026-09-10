from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


DATA_DIR = Path("data")
OUTPUT_DIR = DATA_DIR / "profile"

CLAUDE_FILE = DATA_DIR / "aei_claude_ai_2026-06-26.csv"
API_FILE = DATA_DIR / "aei_1p_api_2026-06-26.csv"


def load_data():
    claude = pd.read_csv(CLAUDE_FILE)
    api = pd.read_csv(API_FILE)

    claude["source"] = "Claude.ai"
    api["source"] = "1P API"

    return pd.concat([claude, api], ignore_index=True)


def plot_collaboration(df):
    metrics = [
        "collaboration_bucket_automation_pct",
        "collaboration_bucket_augmentation_pct",
    ]

    data = df[
        (df["category_name"] == "overall")
        & (df["geo_level"] == "global")
        & (df["metric_id"].isin(metrics))
    ]

    if data.empty:
        print("No collaboration data available.")
        return

    pivot = data.pivot_table(
        index="source",
        columns="metric_id",
        values="value",
        aggfunc="mean",
    )

    pivot.plot(kind="bar")

    plt.title("Automation vs. Augmentation")
    plt.ylabel("Percentage")
    plt.xlabel("Source")
    plt.xticks(rotation=0)
    plt.tight_layout()

    plt.savefig(OUTPUT_DIR / "collaboration.png", dpi=300)
    plt.close()


def plot_use_case(df):
    metrics = [
        "use_case_work_pct",
        "use_case_personal_pct",
        "use_case_coursework_pct",
    ]

    data = df[
        (df["category_name"] == "overall")
        & (df["geo_level"] == "global")
        & (df["metric_id"].isin(metrics))
    ]

    if data.empty:
        print("No use-case data available.")
        return

    pivot = data.pivot_table(
        index="source",
        columns="metric_id",
        values="value",
        aggfunc="mean",
    )

    pivot.plot(kind="bar")

    plt.title("AI Use by Use Case")
    plt.ylabel("Percentage")
    plt.xlabel("Source")
    plt.xticks(rotation=0)
    plt.tight_layout()

    plt.savefig(OUTPUT_DIR / "use_case.png", dpi=300)
    plt.close()


def plot_occupation(df):
    data = df[
        (df["category_name"] == "soc_occupation")
        & (df["geo_level"] == "global")
        & (df["metric_id"] == "pct")
    ]

    if data.empty:
        print("No occupation data available.")
        return

    top = (
        data.groupby(["source", "node_name"])["value"]
        .mean()
        .reset_index()
        .sort_values("value", ascending=False)
        .groupby("source")
        .head(10)
    )

    for source in top["source"].unique():
        subset = top[top["source"] == source]

        plt.figure(figsize=(9, 6))
        plt.barh(subset["node_name"], subset["value"])
        plt.title(f"Top Occupation Usage — {source}")
        plt.xlabel("Percentage")
        plt.gca().invert_yaxis()
        plt.tight_layout()

        filename = (
            "occupation_claude.png"
            if source == "Claude.ai"
            else "occupation_api.png"
        )

        plt.savefig(OUTPUT_DIR / filename, dpi=300)
        plt.close()


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = load_data()

    plot_collaboration(df)
    plot_use_case(df)
    plot_occupation(df)

    print("\nProfile plots created successfully.")
    print(f"Output directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()