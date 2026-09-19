from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


DATA_DIR = Path("data")
OUTPUT_DIR = DATA_DIR / "profile"

CLAUDE_FILE = DATA_DIR / "aei_claude_ai_2026-06-26.csv"
API_FILE = DATA_DIR / "aei_1p_api_2026-06-26.csv"


SOC_MAJOR_GROUPS = {
    "11": "Management",
    "13": "Business and Financial Operations",
    "15": "Computer and Mathematical",
    "17": "Architecture and Engineering",
    "19": "Life, Physical, and Social Science",
    "21": "Community and Social Service",
    "23": "Legal",
    "25": "Educational Instruction and Library",
    "27": "Arts, Design, Entertainment, Sports, and Media",
    "29": "Healthcare Practitioners and Technical",
    "31": "Healthcare Support",
    "33": "Protective Service",
    "35": "Food Preparation and Serving Related",
    "37": "Building and Grounds Cleaning and Maintenance",
    "39": "Personal Care and Service",
    "41": "Sales and Related",
    "43": "Office and Administrative Support",
    "45": "Farming, Fishing, and Forestry",
    "47": "Construction and Extraction",
    "49": "Installation, Maintenance, and Repair",
    "51": "Production",
    "53": "Transportation and Material Moving",
    "55": "Military Specific",
}

COLLAB_METRICS = [
    "collaboration_bucket_automation_pct",
    "collaboration_bucket_augmentation_pct",
]
 


def load_data():
    claude = pd.read_csv(CLAUDE_FILE)
    api = pd.read_csv(API_FILE)
 
    claude["source"] = "Claude.ai"
    api["source"] = "1P API"
 
    return pd.concat([claude, api], ignore_index=True)

def add_major_group(df):
    """Attach a SOC major-occupation-group label, for soc_occupation rows."""
    df = df.copy()
    code = df["node_external_id"].astype(str).str.slice(0, 2)
    is_soc = df["category_name"] == "soc_occupation"
    df["major_group"] = np.where(is_soc, code.map(SOC_MAJOR_GROUPS), np.nan)
    return df


def plot_collaboration(df):
    """Overall automation vs. augmentation split, all traffic, both sources.
    Kept as a baseline, but see plot_automation_work_only for the
    confound-controlled version."""
    data = df[
        (df["category_name"] == "overall")
        & (df["geo_level"] == "global")
        & (df["metric_id"].isin(COLLAB_METRICS))
    ]
 
    if data.empty:
        print("No collaboration data available.")
        return
 
    pivot = data.pivot_table(
        index="source", columns="metric_id", values="value", aggfunc="mean"
    )
 
    ax = pivot.plot(kind="bar")
    for container in ax.containers:
        ax.bar_label(container, fmt="%.1f")
 
    plt.title("Automation vs. Augmentation (All Traffic, Unadjusted)")
    plt.ylabel("Percentage")
    plt.xlabel("Source")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "collaboration.png", dpi=300)
    plt.close()
 
 
def plot_use_case(df):
    metrics = ["use_case_work_pct", "use_case_personal_pct", "use_case_coursework_pct"]
 
    data = df[
        (df["category_name"] == "overall")
        & (df["geo_level"] == "global")
        & (df["metric_id"].isin(metrics))
    ]
 
    if data.empty:
        print("No use-case data available.")
        return
 
    pivot = data.pivot_table(
        index="source", columns="metric_id", values="value", aggfunc="mean"
    )
 
    ax = pivot.plot(kind="bar")
    for container in ax.containers:
        ax.bar_label(container, fmt="%.1f")
 
    plt.title("AI Use by Use Case")
    plt.ylabel("Percentage")
    plt.xlabel("Source")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "use_case.png", dpi=300)
    plt.close()

def plot_occupation(df):
    """Top-10 occupation usage share per source (unchanged from before —
    useful context, but NOT a comparison of automation style)."""
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
 
        filename = "occupation_claude.png" if source == "Claude.ai" else "occupation_api.png"
        plt.savefig(OUTPUT_DIR / filename, dpi=300)
        plt.close()
 
 
def plot_artifact_type_mix(df, top_n=12):
    """NEW — how do businesses (1P API) and individuals (Claude.ai)
    actually use AI, in terms of the kind of output produced? Compares
    the share of traffic going to each artifact type (code, documents,
    spreadsheets, creative writing, presentations, etc.) between sources.
    This is the direct "how do they use it differently" plot — automation
    vs. augmentation shows interaction *style*, this shows task *content*.
    """
    data = df[
        (df["category_name"] == "overall")
        & (df["geo_level"] == "global")
        & (df["metric_id"].str.startswith("artifact_"))
        & (df["metric_id"].str.endswith("_pct"))
    ]
 
    if data.empty:
        print("No artifact-type data available.")
        return
 
    pivot = data.pivot_table(
        index="metric_id", columns="source", values="value", aggfunc="mean"
    ).dropna(how="all")
 
    if pivot.empty:
        print("No artifact-type data present in both sources.")
        return
 
    # keep the top_n types by their largest share in either source
    pivot["_max"] = pivot.max(axis=1)
    pivot = pivot.sort_values("_max", ascending=True).drop(columns="_max").tail(top_n)
 
    pivot.index = (
        pivot.index.str.replace("artifact_", "", regex=False)
        .str.replace("_pct", "", regex=False)
        .str.replace("_", " ", regex=False)
        .str.title()
    )
 
    ax = pivot.plot(kind="barh", figsize=(9, 8))
    plt.xlabel("Share of traffic (%)")
    plt.title(f"Top {top_n} Output Types: Businesses (1P API) vs. Individuals (Claude.ai)")
    plt.legend(title=None)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "artifact_type_mix.png", dpi=300)
    plt.close()
 
    print(f"\nArtifact/output type mix (top {top_n} by max share):")
    print(pivot.round(1).to_string())
 
 
def plot_occupation_category_gap(df, min_group_count=3):
    """FIX #1 — does the automation gap differ by occupation category?
 
    Rolls detailed SOC occupations up to their 23 major groups and
    compares the mean automation share of each group, Claude.ai vs.
    1P API. Answers Q3's second question directly, instead of only
    comparing the handful of exact occupation titles that happen to
    appear in both sources' top-10 lists.
    """
    df = add_major_group(df)
 
    base = df[
        (df["category_name"] == "soc_occupation")
        & (df["geo_level"] == "global")
        & (df["metric_id"] == "collaboration_bucket_automation_pct")
        & (df["major_group"].notna())
    ]
 
    if base.empty:
        print("No occupation-category collaboration data available.")
        return
 
    # require a minimum number of detailed occupations per group per source
    # so a single noisy occupation can't stand in for a whole category
    counts = base.groupby(["source", "major_group"])["node_name"].nunique()
    valid_groups = counts[counts >= min_group_count].index
 
    base = base[
        base.set_index(["source", "major_group"]).index.isin(valid_groups)
    ]
 
    pivot = base.pivot_table(
        index="major_group", columns="source", values="value", aggfunc="mean"
    ).dropna()
 
    if pivot.empty:
        print("No occupation categories present in both sources with enough data.")
        return
 
    pivot["gap"] = pivot["1P API"] - pivot["Claude.ai"]
    pivot = pivot.sort_values("gap")
 
    plt.figure(figsize=(9, 8))
    colors = ["steelblue" if g < 0 else "crimson" for g in pivot["gap"]]
    plt.barh(pivot.index, pivot["gap"], color=colors)
    plt.axvline(0, color="black", linewidth=0.8)
    plt.xlabel("Automation-share gap, percentage points (1P API − Claude.ai)")
    plt.title("Automation Gap by Occupation Category")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "occupation_category_gap.png", dpi=300)
    plt.close()
 
    print("\nAutomation share by occupation category (1P API vs. Claude.ai):")
    print(pivot.round(1).to_string())
 
 
def plot_automation_work_only(df, work_threshold=60.0):
    """FIX #2 — control for the use-case mix confound.
 
    Restricts the automation-vs-augmentation comparison to occupations
    that are predominantly WORK use cases (>= work_threshold%) in BOTH
    sources, usage-weighted. This holds "the task is work" roughly fixed
    across sources, isolating how much of the automation gap survives
    once the personal/coursework mix difference is controlled for.
    """
    base = df[(df["category_name"] == "soc_occupation") & (df["geo_level"] == "global")]
 
    work_share = base[base["metric_id"] == "use_case_work_pct"]
    work_wide = work_share.pivot_table(
        index="node_name", columns="source", values="value", aggfunc="mean"
    ).dropna()
 
    matched_nodes = work_wide[
        (work_wide["Claude.ai"] >= work_threshold) & (work_wide["1P API"] >= work_threshold)
    ].index
 
    if len(matched_nodes) == 0:
        print(f"No occupations exceed {work_threshold}% work-share in both sources.")
        return
 
    usage = (
        base[base["metric_id"] == "pct"]
        .groupby(["source", "node_name"])["value"]
        .mean()
        .rename("usage_pct")
        .reset_index()
    )
 
    collab = base[
        base["metric_id"].isin(COLLAB_METRICS) & base["node_name"].isin(matched_nodes)
    ].merge(usage, on=["source", "node_name"], how="left")
    collab["usage_pct"] = collab["usage_pct"].fillna(0)
 
    def wavg(g):
        weights = g["usage_pct"].to_numpy() + 1e-9  # avoid all-zero weights
        return np.average(g["value"].to_numpy(), weights=weights)
 
    result = (
        collab.groupby(["source", "metric_id"])
        .apply(wavg, include_groups=False)
        .rename("value")
        .reset_index()
        .pivot(index="source", columns="metric_id", values="value")
    )
 
    ax = result.plot(kind="bar")
    for container in ax.containers:
        ax.bar_label(container, fmt="%.1f")
 
    plt.title(
        f"Automation vs. Augmentation\n(Work-Dominant Occupations Only, "
        f"\u2265{work_threshold:.0f}% Work Share, Usage-Weighted)"
    )
    plt.ylabel("Percentage")
    plt.xlabel("Source")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "collaboration_work_only.png", dpi=300)
    plt.close()
 
    print(f"\nMatched {len(matched_nodes)} occupations with >= {work_threshold}% "
          f"work share in both sources:")
    print(result.round(1).to_string())
 
 
def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
 
    df = load_data()
 
    plot_collaboration(df)
    plot_use_case(df)
    plot_occupation(df)
    plot_artifact_type_mix(df)
    plot_occupation_category_gap(df)
    plot_automation_work_only(df)
 
    print("\nProfile plots created successfully.")
    print(f"Output directory: {OUTPUT_DIR}")
 
 
if __name__ == "__main__":
    main()