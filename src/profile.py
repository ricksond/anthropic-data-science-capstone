from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
DATA_DIR = Path("data")
OUTPUT_DIR = DATA_DIR / "profile"

CLAUDE_FILE = DATA_DIR / "aei_claude_ai_2026-06-26.csv"
API_FILE = DATA_DIR / "aei_1p_api_2026-06-26.csv"

# 2018 SOC major-group codes. Detailed SOC occupation codes begin with the
# two-digit major-group code (for example, "13-1199.06" -> "13").
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

REFERENCE_GROUP = "Computer and Mathematical"
MIN_OCCUPATIONS_PER_GROUP = 3


# ---------------------------------------------------------------------------
# Hypotheses
# ---------------------------------------------------------------------------
HYPOTHESES = {
    "H1": (
        "The distribution of AI output/artifact types differs between "
        "Claude.ai and first-party API usage.",
        "Compare the reported artifact-type percentages across sources. "
        "This is a descriptive comparison because the released aggregate "
        "percentages do not provide the underlying category counts needed "
        "for a defensible inferential test."
    ),
    "H2": (
        "The automation share of interactions differs between Claude.ai "
        "and first-party API usage.",
        "The adjusted 1P API minus Claude.ai automation gap has a 95% "
        "confidence interval that excludes zero in the occupation-level "
        "WLS model, controlling for occupation category and work-use share."
    ),
}


# ---------------------------------------------------------------------------
# Data loading and structural checks
# ---------------------------------------------------------------------------
def load_data():
    """Load the two release files and label each row by access method."""
    if not CLAUDE_FILE.exists():
        raise FileNotFoundError(f"Claude.ai data file not found: {CLAUDE_FILE}")
    if not API_FILE.exists():
        raise FileNotFoundError(f"1P API data file not found: {API_FILE}")

    claude = pd.read_csv(CLAUDE_FILE)
    api = pd.read_csv(API_FILE)

    claude["source"] = "Claude.ai"
    api["source"] = "1P API"

    return pd.concat([claude, api], ignore_index=True)


def add_major_group(df):
    """Attach a broad SOC major-group label to detailed occupation rows."""
    df = df.copy()
    code = df["node_external_id"].astype(str).str.slice(0, 2)
    is_soc = df["category_name"].eq("soc_occupation")
    df["major_group"] = np.where(is_soc, code.map(SOC_MAJOR_GROUPS), np.nan)
    return df


def keep_detailed(data):
    """Keep level-0 detailed occupations, not level-1 aggregate rows."""
    if "hierarchy_level" in data.columns:
        return data[data["hierarchy_level"] == 0].copy()
    raise KeyError(
        "Expected 'hierarchy_level' in the release data. "
        "Cannot safely distinguish detailed occupations from aggregates."
    )


def check_data_structure(df):
    """Print release months, occupation hierarchy levels, and usage totals."""
    required = {
        "source", "date_start", "category_name", "geo_level", "metric_id",
        "value", "hierarchy_level",
    }
    missing = required.difference(df.columns)
    if missing:
        raise KeyError(f"Missing expected data columns: {sorted(missing)}")

    print("\n" + "=" * 72)
    print("DATA STRUCTURE CHECK")
    print("=" * 72)

    print("\nMonths present (date_start) by source:")
    print(df.groupby("source")["date_start"].unique().to_string())

    soc = df[
        (df["category_name"] == "soc_occupation")
        & (df["geo_level"] == "global")
    ]
    print("\nsoc_occupation rows by source x hierarchy_level:")
    print(
        soc.groupby(["source", "hierarchy_level"])
        .size()
        .unstack(fill_value=0)
        .to_string()
    )

    pct = soc[soc["metric_id"] == "pct"]
    sums = (
        pct.groupby(["source", "date_start", "hierarchy_level"])["value"]
        .sum()
        .unstack("hierarchy_level")
        .round(1)
    )
    print("\nSum of occupation usage 'pct' by source, month, and hierarchy level:")
    print(sums.to_string())
    print("\nOccupation-level modeling uses hierarchy_level == 0 only.")


# ---------------------------------------------------------------------------
# H1: Output/artifact-type comparison
# ---------------------------------------------------------------------------
def build_output_type_table(df):
    """Return mean artifact-type percentages by source and their difference.

    The release contains April and May rows. We average the monthly values
    for each source/metric rather than summing the months.
    """
    data = df[
        (df["category_name"] == "overall")
        & (df["geo_level"] == "global")
        & df["metric_id"].astype(str).str.startswith("artifact_")
        & df["metric_id"].astype(str).str.endswith("_pct")
    ].copy()

    if data.empty:
        raise ValueError(
            "No artifact_*_pct metrics were found for overall/global data. "
            "Check the metric names in the downloaded release."
        )

    table = (
        data.groupby(["metric_id", "source"], as_index=False)["value"]
        .mean()
        .pivot(index="metric_id", columns="source", values="value")
    )

    required_sources = {"Claude.ai", "1P API"}
    if not required_sources.issubset(table.columns):
        raise ValueError(
            "Artifact-type metrics must be present for both Claude.ai and "
            f"1P API. Found columns: {list(table.columns)}"
        )

    table = table.dropna(subset=["Claude.ai", "1P API"]).copy()
    table["api_minus_claude_pp"] = table["1P API"] - table["Claude.ai"]
    table.index = (
        table.index.str.replace("artifact_", "", regex=False)
        .str.replace("_pct", "", regex=False)
        .str.replace("_", " ", regex=False)
        .str.title()
    )
    table.index.name = "output_type"
    return table.sort_values("api_minus_claude_pp", ascending=False)


def plot_output_type_mix(df):
    """Plot and export the H1 output-type comparison."""
    table = build_output_type_table(df)
    table.to_csv(OUTPUT_DIR / "h1_output_type_comparison.csv")

    plot_data = table[["Claude.ai", "1P API"]].sort_values(
        "1P API", ascending=True
    )
    ax = plot_data.plot(kind="barh", figsize=(10, max(6, 0.42 * len(plot_data))))
    ax.set_xlabel("Reported share (%)")
    ax.set_ylabel("Output/artifact type")
    ax.set_title("AI Output-Type Mix: Claude.ai vs. First-Party API")
    ax.legend(title="Access method")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "h1_output_type_mix.png", dpi=300)
    plt.close()

    print("\nH1 — output/artifact-type comparison (monthly mean percentages):")
    print(table.round(2).to_string())
    print(
        "\nH1 interpretation: compare the category profile and percentage-point "
        "differences descriptively. Do not report a p-value from these "
        "aggregated percentages without underlying counts or uncertainty data."
    )
    return table


# ---------------------------------------------------------------------------
# Supporting descriptive plots for H2
# ---------------------------------------------------------------------------
def plot_collaboration_overall(df):
    """Plot overall automation and augmentation shares for both sources."""
    data = df[
        (df["category_name"] == "overall")
        & (df["geo_level"] == "global")
        & df["metric_id"].isin(COLLAB_METRICS)
    ]

    if data.empty:
        print("No overall collaboration metrics available.")
        return

    pivot = (
        data.groupby(["source", "metric_id"])["value"]
        .mean()
        .unstack("metric_id")
        .reindex(["Claude.ai", "1P API"])
    )
    pivot = pivot.rename(
        columns={
            "collaboration_bucket_automation_pct": "Automation",
            "collaboration_bucket_augmentation_pct": "Augmentation",
        }
    )
    pivot.to_csv(OUTPUT_DIR / "h2_overall_collaboration.csv")

    ax = pivot.plot(kind="bar", figsize=(8, 6))
    for container in ax.containers:
        ax.bar_label(container, fmt="%.1f")
    ax.set_title("Automation vs. Augmentation — All Traffic")
    ax.set_ylabel("Reported share (%)")
    ax.set_xlabel("Access method")
    ax.tick_params(axis="x", rotation=0)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "h2_collaboration_overall.png", dpi=300)
    plt.close()

    print("\nOverall collaboration split (monthly mean percentages):")
    print(pivot.round(2).to_string())


def plot_use_case_context(df):
    """Show work, personal, and coursework mix as descriptive context."""
    metrics = [
        "use_case_work_pct",
        "use_case_personal_pct",
        "use_case_coursework_pct",
    ]
    data = df[
        (df["category_name"] == "overall")
        & (df["geo_level"] == "global")
        & df["metric_id"].isin(metrics)
    ]

    if data.empty:
        print("No overall use-case metrics available.")
        return

    pivot = (
        data.groupby(["source", "metric_id"])["value"]
        .mean()
        .unstack("metric_id")
        .reindex(["Claude.ai", "1P API"])
    )
    pivot = pivot.rename(
        columns={
            "use_case_work_pct": "Work",
            "use_case_personal_pct": "Personal",
            "use_case_coursework_pct": "Coursework",
        }
    )
    pivot.to_csv(OUTPUT_DIR / "use_case_context.csv")

    ax = pivot.plot(kind="bar", figsize=(8, 6))
    for container in ax.containers:
        ax.bar_label(container, fmt="%.1f")
    ax.set_title("Reported AI Use-Case Mix")
    ax.set_ylabel("Reported share (%)")
    ax.set_xlabel("Access method")
    ax.tick_params(axis="x", rotation=0)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "use_case_context.png", dpi=300)
    plt.close()


# ---------------------------------------------------------------------------
# H2: Occupation-level dataset and automation comparison
# ---------------------------------------------------------------------------
def build_regression_dataset(df, min_group_count=MIN_OCCUPATIONS_PER_GROUP):
    """Build one row per source x detailed occupation.

    April and May values are averaged first. Usage share is used as a
    weighting proxy, not as a raw sample size. Occupation major group and
    work-use share are included as covariates in the H2 model.
    """
    data = add_major_group(df)
    base = data[
        (data["category_name"] == "soc_occupation")
        & (data["geo_level"] == "global")
        & data["major_group"].notna()
    ]
    base = keep_detailed(base)

    keys = ["source", "major_group", "node_name"]

    def metric_mean(metric_id):
        subset = base[base["metric_id"] == metric_id]
        return subset.groupby(keys)["value"].mean()

    automation = metric_mean(
        "collaboration_bucket_automation_pct"
    ).rename("automation_pct")
    work_share = metric_mean("use_case_work_pct").rename("work_share_pct")
    usage = metric_mean("pct").rename("usage_pct")

    reg = pd.concat([automation, work_share, usage], axis=1).dropna().reset_index()

    # Retain categories represented by at least min_group_count detailed
    # occupations in each source, so the comparison uses matched categories.
    counts = reg.groupby(["source", "major_group"])["node_name"].nunique()
    valid_groups = counts[counts >= min_group_count].index
    reg = reg[
        reg.set_index(["source", "major_group"]).index.isin(valid_groups)
    ].copy()

    if reg.empty:
        raise ValueError(
            "The H2 regression dataset is empty after filtering. "
            "Check the metric names and minimum occupation threshold."
        )

    if set(reg["source"].unique()) != {"Claude.ai", "1P API"}:
        raise ValueError("H2 regression requires both sources.")

    reg["source_api"] = (reg["source"] == "1P API").astype(int)
    reg["major_group"] = reg["major_group"].astype(str)
    return reg


def _fit_wls(formula, reg, weighted=True):
    """Fit a model with standard errors clustered by detailed occupation."""
    import statsmodels.formula.api as smf

    data = reg.reset_index(drop=True).copy()
    groups = pd.factorize(data["node_name"])[0]

    if weighted:
        model = smf.wls(
            formula,
            data=data,
            weights=data["usage_pct"].clip(lower=1e-6),
        )
    else:
        model = smf.ols(formula, data=data)

    return model.fit(
        cov_type="cluster",
        cov_kwds={"groups": groups},
    )


def _fit_fractional_logit(reg):
    """Fit an unweighted fractional-logit robustness model."""
    import patsy
    import statsmodels.api as sm

    data = reg.reset_index(drop=True).copy()
    y = (data["automation_pct"] / 100).clip(1e-4, 1 - 1e-4)
    formula = "source_api + C(major_group) + work_share_pct"
    X = patsy.dmatrix(formula, data=data, return_type="dataframe")
    groups = pd.factorize(data["node_name"])[0]

    model = sm.GLM(y, X, family=sm.families.Binomial())
    return model.fit(
        cov_type="cluster",
        cov_kwds={"groups": groups},
    )


def plot_work_dominant_occupations(df, work_threshold=60.0):
    """Sensitivity-style descriptive comparison among work-dominant jobs.

    An occupation is retained only when its work-use share meets the
    threshold in both sources. The result is usage-weighted.
    """
    base = df[
        (df["category_name"] == "soc_occupation")
        & (df["geo_level"] == "global")
    ]
    base = keep_detailed(base)

    work = base[base["metric_id"] == "use_case_work_pct"]
    work_wide = (
        work.groupby(["source", "node_name"])["value"]
        .mean()
        .unstack("source")
        .dropna()
    )

    required = {"Claude.ai", "1P API"}
    if not required.issubset(work_wide.columns):
        print("Cannot build work-dominant comparison: one source is missing.")
        return

    matched = work_wide[
        (work_wide["Claude.ai"] >= work_threshold)
        & (work_wide["1P API"] >= work_threshold)
    ].index

    if len(matched) == 0:
        print(f"No occupations meet the {work_threshold:.0f}% work threshold.")
        return

    usage = (
        base[base["metric_id"] == "pct"]
        .groupby(["source", "node_name"])["value"]
        .mean()
        .rename("usage_pct")
        .reset_index()
    )
    collab = base[
        base["metric_id"].isin(COLLAB_METRICS)
        & base["node_name"].isin(matched)
    ].merge(usage, on=["source", "node_name"], how="left")

    rows = []
    for (source, metric), group in collab.groupby(["source", "metric_id"]):
        weights = group["usage_pct"].fillna(0).clip(lower=0).to_numpy()
        values = group["value"].to_numpy()
        if weights.sum() == 0:
            estimate = float(np.mean(values))
        else:
            estimate = float(np.average(values, weights=weights))
        rows.append(
            {"source": source, "metric_id": metric, "value": estimate}
        )

    result = (
        pd.DataFrame(rows)
        .pivot(index="source", columns="metric_id", values="value")
        .reindex(["Claude.ai", "1P API"])
    )
    result.to_csv(OUTPUT_DIR / "h2_work_dominant_occupations.csv")

    display = result.rename(
        columns={
            "collaboration_bucket_automation_pct": "Automation",
            "collaboration_bucket_augmentation_pct": "Augmentation",
        }
    )
    ax = display.plot(kind="bar", figsize=(8, 6))
    for container in ax.containers:
        ax.bar_label(container, fmt="%.1f")
    ax.set_title(
        f"Collaboration Split in Work-Dominant Occupations "
        f"(at least {work_threshold:.0f}% work share in both sources)"
    )
    ax.set_ylabel("Usage-weighted reported share (%)")
    ax.set_xlabel("Access method")
    ax.tick_params(axis="x", rotation=0)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "h2_work_dominant_occupations.png", dpi=300)
    plt.close()

    print(
        f"\nWork-dominant comparison: {len(matched)} matched detailed occupations"
    )
    print(display.round(2).to_string())


def test_h2_automation(reg, results):
    """Test whether the adjusted automation share differs by access method."""
    base_formula = "automation_pct ~ source_api + C(major_group)"
    adjusted_formula = base_formula + " + work_share_pct"

    wls_unadjusted = _fit_wls(base_formula, reg, weighted=True)
    wls_adjusted = _fit_wls(adjusted_formula, reg, weighted=True)
    ols_adjusted = _fit_wls(adjusted_formula, reg, weighted=False)
    fractional = _fit_fractional_logit(reg)

    gap_unadjusted = float(wls_unadjusted.params["source_api"])
    gap_adjusted = float(wls_adjusted.params["source_api"])
    ci_low, ci_high = wls_adjusted.conf_int().loc["source_api"]
    p_wls = float(wls_adjusted.pvalues["source_api"])
    p_ols = float(ols_adjusted.pvalues["source_api"])
    p_fractional = float(fractional.pvalues["source_api"])

    work_share_change = (
        (gap_unadjusted - gap_adjusted) / gap_unadjusted * 100
        if gap_unadjusted != 0
        else np.nan
    )

    print("\n" + "=" * 72)
    print("H2 — AUTOMATION SHARE DIFFERENCE")
    print("=" * 72)
    print(f"Regression rows: {len(reg)} source x occupation observations")
    print(f"Distinct detailed occupations: {reg['node_name'].nunique()}")
    print(f"Gap adjusted for occupation category: {gap_unadjusted:.2f} pp")
    print(
        "Gap adjusted for occupation category + work share: "
        f"{gap_adjusted:.2f} pp "
        f"(95% CI {ci_low:.2f} to {ci_high:.2f}; WLS p = {p_wls:.4g})"
    )
    print(f"Change after adding work share: {work_share_change:.1f}%")
    print("\nRobustness checks (same adjusted covariates):")
    print(f"  WLS, usage-weighted, occupation-clustered SE: p = {p_wls:.4g}")
    print(f"  OLS, unweighted, occupation-clustered SE:     p = {p_ols:.4g}")
    print(f"  Fractional logit, unweighted, clustered SE:   p = {p_fractional:.4g}")
    print(
        "\nInterpretation: the WLS coefficient is the adjusted percentage-point "
        "difference (1P API minus Claude.ai). Usage share is a weighting proxy, "
        "not an observed sample size."
    )

    # Export model comparisons in a compact, reproducible table.
    model_table = pd.DataFrame(
        [
            {
                "model": "WLS_adjusted",
                "api_minus_claude_estimate": gap_adjusted,
                "ci_95_low": ci_low,
                "ci_95_high": ci_high,
                "p_value": p_wls,
                "weighted_by_usage_share": True,
            },
            {
                "model": "OLS_adjusted",
                "api_minus_claude_estimate": float(
                    ols_adjusted.params["source_api"]
                ),
                "ci_95_low": float(
                    ols_adjusted.conf_int().loc["source_api", 0]
                ),
                "ci_95_high": float(
                    ols_adjusted.conf_int().loc["source_api", 1]
                ),
                "p_value": p_ols,
                "weighted_by_usage_share": False,
            },
        ]
    )
    model_table.to_csv(OUTPUT_DIR / "h2_automation_model_comparison.csv", index=False)

    supported = bool(ci_low > 0 or ci_high < 0)
    results.append(
        {
            "hypothesis": "H2",
            "finding": (
                f"Adjusted 1P API - Claude.ai automation gap = "
                f"{gap_adjusted:.2f} pp "
                f"(95% CI {ci_low:.2f}, {ci_high:.2f})"
            ),
            "p_value_wls": p_wls,
            "assessment": "Supported" if supported else "Not supported",
            "note": (
                f"OLS p={p_ols:.4g}; fractional-logit p={p_fractional:.4g}. "
                "Observational association; not a causal business-versus-consumer "
                "effect. API and Claude.ai are access-method proxies."
            ),
        }
    )

    return {
        "gap_unadjusted": gap_unadjusted,
        "gap_adjusted": gap_adjusted,
        "ci_low": float(ci_low),
        "ci_high": float(ci_high),
        "p_value": p_wls,
    }


# ---------------------------------------------------------------------------
# Hypothesis summary and execution
# ---------------------------------------------------------------------------
def write_hypothesis_summary(output_table, h2_result):
    """Write the two-hypothesis summary without inventing an H1 p-value."""
    h1_assessment = (
        "Descriptive comparison completed"
        if output_table is not None and not output_table.empty
        else "Not evaluated"
    )
    h1_note = (
        "Artifact-type percentages are compared by source and exported. "
        "No inferential p-value is reported because underlying counts and "
        "sampling uncertainty are not available in these aggregate metrics."
    )

    rows = [
        {
            "hypothesis": "H1",
            "finding": (
                "Output/artifact-type percentages compared across Claude.ai "
                "and 1P API"
            ),
            "p_value_wls": np.nan,
            "assessment": h1_assessment,
            "note": h1_note,
        }
    ]

    if h2_result is not None:
        # H2's full model result is already represented in the model output.
        # The assessment and detailed estimate are recorded by test_h2_automation.
        pass

    summary_path = OUTPUT_DIR / "hypothesis_summary.csv"
    if h2_result is None:
        pd.DataFrame(rows).to_csv(summary_path, index=False)
    else:
        h2_path = OUTPUT_DIR / "h2_hypothesis_result.csv"
        # test_h2_automation writes the H2 result to this file in main().
        h2_row = pd.read_csv(h2_path)
        pd.concat([pd.DataFrame(rows), h2_row], ignore_index=True).to_csv(
            summary_path, index=False
        )


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading Anthropic Economic Index release data...")
    df = load_data()
    check_data_structure(df)

    print("\nGenerating H1 output-type analysis...")
    output_table = plot_output_type_mix(df)

    print("\nGenerating H2 descriptive comparisons...")
    plot_collaboration_overall(df)
    plot_use_case_context(df)
    plot_work_dominant_occupations(df, work_threshold=60.0)

    print("\nFitting H2 occupation-adjusted models...")
    try:
        reg = build_regression_dataset(df)
        results = []
        h2_result = test_h2_automation(reg, results)
        pd.DataFrame(results).to_csv(
            OUTPUT_DIR / "h2_hypothesis_result.csv", index=False
        )
        write_hypothesis_summary(output_table, h2_result)
    except ImportError as exc:
        print(f"\nSkipping H2 inferential model — missing package: {exc}")
        print("Install with: pip install statsmodels patsy scipy")
        write_hypothesis_summary(output_table, None)
    except Exception as exc:
        print(f"\nH2 model failed: {type(exc).__name__}: {exc}")
        write_hypothesis_summary(output_table, None)

    print("\n" + "=" * 72)
    print("PROFILE COMPLETE")
    print("=" * 72)
    print(f"Outputs saved to: {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()