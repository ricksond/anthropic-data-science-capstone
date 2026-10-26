from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


DATA_DIR = Path("data")
OUTPUT_DIR = DATA_DIR / "profile"

CLAUDE_FILE = DATA_DIR / "aei_claude_ai_2026-06-26.csv"
API_FILE = DATA_DIR / "aei_1p_api_2026-06-26.csv"

# 2018 SOC major-group codes -> names. node_external_id for soc_occupation
# rows is a detailed SOC code like "13-1199.06"; the first two digits are
# the major group. This lets us roll ~800 detailed occupations up into the
# ~23 broad "occupation categories" Q3 asks about, instead of only being
# able to compare the handful of exact titles that show up in both top-10s.
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

# The release documentation says soc_occupation has two hierarchy levels:
# level 0 = detailed occupation, level 1 = major group (an aggregate of the
# detailed occupations beneath it). Mixing them treats a group total as if it
# were one more occupation: it double-counts usage (category usage sums come
# out near 190% instead of ~100%) and, because regression weights are usage
# shares, the group row becomes the heaviest-weighted "occupation" in its own
# category. With DETAILED_ONLY = True every SOC analysis keeps level 0 only.
# Set it to False to reproduce the earlier (mixed-level) numbers for comparison.
DETAILED_ONLY = True

# Hypothesis-test settings
REFERENCE_GROUP = "Computer and Mathematical"
ALPHA = 0.05


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


def keep_detailed(data):
    """Drop level-1 (major-group aggregate) SOC rows when DETAILED_ONLY is on."""
    if DETAILED_ONLY and "hierarchy_level" in data.columns:
        return data[data["hierarchy_level"] == 0]
    return data


def check_data_structure(df):
    """Print the facts the analysis silently depends on, so they can be
    verified instead of assumed:
      1. which months are present (the release covers April AND May 2026,
         so any 'duplicate' rows per node are really two different months),
      2. which hierarchy levels exist for soc_occupation, and
      3. whether usage 'pct' sums to ~100% within a source/month/level
         (if it sums to ~200% across levels, levels are being double counted).
    """
    print("\n" + "=" * 70)
    print("DATA STRUCTURE CHECK")
    print("=" * 70)

    print("\nMonths present (date_start) by source:")
    print(df.groupby("source")["date_start"].unique().to_string())

    soc = df[(df["category_name"] == "soc_occupation") & (df["geo_level"] == "global")]
    print("\nsoc_occupation rows by source x hierarchy_level:")
    print(soc.groupby(["source", "hierarchy_level"]).size().unstack(fill_value=0).to_string())

    print("\nExample node names at each hierarchy level (source = 1P API):")
    for lvl, g in soc[soc["source"] == "1P API"].groupby("hierarchy_level"):
        names = g["node_name"].drop_duplicates().head(4).tolist()
        print(f"  level {lvl}: {names}")

    pct = soc[soc["metric_id"] == "pct"]
    sums = (
        pct.groupby(["source", "date_start", "hierarchy_level"])["value"]
        .sum()
        .unstack("hierarchy_level")
        .round(1)
    )
    print("\nSum of 'pct' across soc_occupation nodes (each level should be ~100 on its own):")
    print(sums.to_string())
    print(f"\nDETAILED_ONLY = {DETAILED_ONLY} "
          f"({'level 0 only' if DETAILED_ONLY else 'all levels mixed'})")


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
    data = keep_detailed(data)

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
    base = keep_detailed(base)

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

    # Grouped bar of the actual automation % per source, not just the gap.
    # The gap alone can't distinguish "95% vs 50%" from "60% vs 15%" — same
    # gap, very different stories — and since every category has a positive
    # gap here, a diverging (red/blue by sign) chart would render as a single
    # color throughout, which hides more than it shows. This version plots
    # both sources' actual levels, still sorted by gap size, and annotates
    # the gap at the end of each pair of bars.
    fig, ax = plt.subplots(figsize=(10, 9))
    y = np.arange(len(pivot))
    bar_h = 0.38

    ax.barh(y + bar_h / 2, pivot["1P API"], height=bar_h, label="1P API", color="#1f77b4")
    ax.barh(y - bar_h / 2, pivot["Claude.ai"], height=bar_h, label="Claude.ai", color="#ff7f0e")

    ax.set_yticks(y)
    ax.set_yticklabels(pivot.index)
    ax.set_xlabel("Automation share of traffic (%)")
    ax.set_title("Automation Share by Occupation Category\n(sorted by gap size; label = gap in percentage points)")
    ax.set_xlim(0, 108)
    ax.legend(loc="lower right")

    for yi, (api_val, claude_val, gap) in enumerate(
        zip(pivot["1P API"], pivot["Claude.ai"], pivot["gap"])
    ):
        ax.text(max(api_val, claude_val) + 1.5, yi, f"+{gap:.0f} pts",
                 va="center", fontsize=8, color="dimgray")

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "occupation_category_gap.png", dpi=300)
    plt.close()

    print("\nAutomation share by occupation category (1P API vs. Claude.ai):")
    print(pivot.round(1).to_string())


def plot_gap_vs_usage(df, min_group_count=3):
    """NEXT STEP — is the automation gap smaller in categories that see
    more usage (a "maturity"/convergence story), or was the Computer and
    Mathematical exception (highest usage, one of the smallest gaps) just
    a one-off? Plots the automation gap for each of the 23 occupation
    categories against that category's total usage share, with a trend
    line and Pearson correlation coefficient.

    Usage share here is the sum of the 'pct' usage metric across all
    detailed SOC occupations in a category, averaged across the two
    sources, as a proxy for "how much this category gets used overall."
    This is an approximation, not an exact combined-traffic figure — flagged
    in the printed output as a limitation.
    """
    df = add_major_group(df)

    base = df[
        (df["category_name"] == "soc_occupation")
        & (df["geo_level"] == "global")
        & (df["major_group"].notna())
    ]
    base = keep_detailed(base)

    collab = base[base["metric_id"] == "collaboration_bucket_automation_pct"]
    counts = collab.groupby(["source", "major_group"])["node_name"].nunique()
    valid_groups = counts[counts >= min_group_count].index
    collab = collab[collab.set_index(["source", "major_group"]).index.isin(valid_groups)]

    gap_pivot = collab.pivot_table(
        index="major_group", columns="source", values="value", aggfunc="mean"
    ).dropna()

    if gap_pivot.empty:
        print("No matched occupation categories for gap-vs-usage comparison.")
        return

    gap_pivot["gap"] = gap_pivot["1P API"] - gap_pivot["Claude.ai"]

    # usage share per category: sum detailed-occupation usage_pct within a
    # category, per source, then average the two sources as a combined proxy.
    # IMPORTANT: average each node's value across duplicate date rows FIRST
    # (the data has two overlapping monthly rows per node) before summing
    # across nodes — summing raw rows double-counts and was producing
    # category totals over 100%, as seen in the first run of this chart.
    usage = base[base["metric_id"] == "pct"]
    node_usage = usage.groupby(["source", "major_group", "node_name"])["value"].mean()
    usage_by_group_source = node_usage.groupby(["source", "major_group"]).sum()
    usage_total = usage_by_group_source.groupby("major_group").mean()

    merged = gap_pivot.join(usage_total.rename("usage_share")).dropna()

    if len(merged) < 3:
        print("Not enough matched categories for a usage-vs-gap comparison.")
        return

    x = merged["usage_share"].to_numpy()
    y = merged["gap"].to_numpy()
    r = np.corrcoef(x, y)[0, 1]

    coeffs = np.polyfit(x, y, 1)
    trend_x = np.linspace(x.min(), x.max(), 50)
    trend_y = np.polyval(coeffs, trend_x)

    plt.figure(figsize=(9, 7))
    plt.scatter(x, y, s=60, color="#1f77b4", zorder=3)
    plt.plot(trend_x, trend_y, "--", color="gray", zorder=2, label=f"trend (r = {r:.2f})")

    for name, xi, yi in zip(merged.index, x, y):
        plt.annotate(name, (xi, yi), fontsize=7, xytext=(4, 4), textcoords="offset points")

    plt.xlabel("Total category usage share (%, proxy — summed across detailed occupations)")
    plt.ylabel("Automation gap, percentage points (1P API − Claude.ai)")
    plt.title("Does the Automation Gap Shrink in Higher-Usage Categories?")
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "gap_vs_usage.png", dpi=300)
    plt.close()

    print(f"\nGap vs. usage-share correlation: Pearson r = {r:.2f}")
    print("(negative r = higher-usage categories tend to have smaller gaps, "
          "supporting a maturity/convergence story; r near 0 = no relationship, "
          "Computer and Mathematical would be a one-off.)")
    print(merged.round(1).sort_values("usage_share", ascending=False).to_string())


def plot_automation_work_only(df, work_threshold=60.0):
    """FIX #2 — control for the use-case mix confound.

    Restricts the automation-vs-augmentation comparison to occupations
    that are predominantly WORK use cases (>= work_threshold%) in BOTH
    sources, usage-weighted. This holds "the task is work" roughly fixed
    across sources, isolating how much of the automation gap survives
    once the personal/coursework mix difference is controlled for.
    """
    base = df[(df["category_name"] == "soc_occupation") & (df["geo_level"] == "global")]
    base = keep_detailed(base)

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


def build_regression_dataset(df, min_group_count=3):
    """Shared per-occupation dataset for the statistical models below: one
    row per (source, major_group, node_name) with the automation share
    (outcome), work-use-case share (confound covariate), and usage share
    (regression weight, since we have no raw sample sizes — this is the
    standard proxy for how much to trust each occupation's estimate).

    The release holds two calendar months (April and May 2026); each
    occupation's value is averaged over them.
    """
    df = add_major_group(df)
    base = df[
        (df["category_name"] == "soc_occupation")
        & (df["geo_level"] == "global")
        & (df["major_group"].notna())
    ]
    base = keep_detailed(base)

    keys = ["source", "major_group", "node_name"]

    def node_mean(metric_id):
        s = base[base["metric_id"] == metric_id]
        return s.groupby(keys)["value"].mean()

    automation = node_mean("collaboration_bucket_automation_pct").rename("automation_pct")
    work_share = node_mean("use_case_work_pct").rename("work_share_pct")
    usage = node_mean("pct").rename("usage_pct")

    reg = pd.concat([automation, work_share, usage], axis=1).dropna().reset_index()

    # same category-size floor used in plot_occupation_category_gap, so the
    # model is fit on the same matched set of categories shown in that chart
    counts = reg.groupby(["source", "major_group"])["node_name"].nunique()
    valid = counts[counts >= min_group_count].index
    reg = reg[reg.set_index(["source", "major_group"]).index.isin(valid)]

    reg["source_api"] = (reg["source"] == "1P API").astype(int)
    reg["major_group"] = reg["major_group"].astype("category")
    return reg


def run_wls_model(reg, reference_group="Computer and Mathematical"):
    """PRIMARY MODEL — weighted least squares:

        automation_pct ~ source_api * major_group + work_share_pct

    weighted by usage share. `source_api` is the automation gap (API vs.
    Claude.ai) holding category and work-share fixed — a formal version of
    the §1 comparison. The source_api × major_group interaction terms test
    whether specific categories' gaps differ significantly from the
    reference category's gap (set to Computer and Mathematical, the
    highest-usage category, so every interaction reads as "how much bigger/
    smaller this category's gap is, relative to Computer and Mathematical").
    work_share_pct is the confound control from plot_automation_work_only,
    built into the model instead of a separate restricted sample.

    Requires `statsmodels` (pip install statsmodels).
    """
    import statsmodels.formula.api as smf

    reg = reg.copy()
    reg["major_group"] = reg["major_group"].cat.reorder_categories(
        [reference_group] + [c for c in reg["major_group"].cat.categories if c != reference_group]
    )

    formula = (
        "automation_pct ~ source_api * C(major_group, Treatment(reference='"
        f"{reference_group}')) + work_share_pct"
    )
    model = smf.wls(formula, data=reg, weights=reg["usage_pct"] + 1e-6)
    result = model.fit()

    print("\n" + "=" * 70)
    print("WLS MODEL (primary): automation_pct ~ source * category + work_share")
    print("=" * 70)
    print(result.summary())
    return result


def run_beta_model(reg, reference_group="Computer and Mathematical"):
    """ROBUSTNESS CHECK — beta regression.

    automation_pct is a bounded percentage (0-100), so an ordinary linear
    model can in principle predict outside that range and its errors are
    not actually homoscedastic/normal near the boundaries. Beta regression
    is the textbook-correct model for a bounded proportion outcome. Same
    right-hand side as the WLS model; if the two models agree on which
    interaction terms are significant, that's good evidence the WLS result
    isn't an artifact of its linear-model assumptions.

    Requires `statsmodels` >= 0.13 (for statsmodels.othermod.betareg) and
    `patsy` (pip install statsmodels patsy).
    """
    import patsy
    from statsmodels.othermod.betareg import BetaModel

    reg = reg.copy()
    reg["major_group"] = reg["major_group"].cat.reorder_categories(
        [reference_group] + [c for c in reg["major_group"].cat.categories if c != reference_group]
    )

    # beta regression requires the outcome strictly inside (0, 1); clip the
    # handful of exact 0/100 values away from the boundary
    y = (reg["automation_pct"] / 100).clip(1e-4, 1 - 1e-4)

    formula = (
        "source_api * C(major_group, Treatment(reference='"
        f"{reference_group}')) + work_share_pct"
    )
    X = patsy.dmatrix(formula, data=reg, return_type="dataframe")

    model = BetaModel(y, X)
    result = model.fit()

    print("\n" + "=" * 70)
    print("BETA REGRESSION MODEL (robustness check)")
    print("=" * 70)
    print(result.summary())
    return result


# ===========================================================================
# HYPOTHESES
#
# Written down BEFORE the corrected (level-0-only) re-run, each with a
# prediction and a rule for what counts as support, so the results can be
# judged against something stated in advance rather than fitted afterwards.
# ===========================================================================
HYPOTHESES = {
    "H1": ("Firms are more automation-heavy, and the use-case mix does not "
           "explain it. After controlling for occupation category and work "
           "share, 1P API automation share exceeds Claude.ai's.",
           "Adjusted gap > 0 with a 95% CI that excludes 0, AND adding work "
           "share shrinks the gap by < 25%."),
    "H2": ("The gap is not the same in every occupation category.",
           "Omnibus test that all source x category interactions are zero is "
           "rejected (p < 0.05) in all three fits: weighted WLS, unweighted OLS, "
           "and unweighted fractional logit."),
    "H3": ("Category-to-category variation in the gap comes mainly from "
           "Claude.ai (individuals), not from the API (firms automate "
           "uniformly).",
           "Claude.ai accounts for > 75% of the variance of the gap across categories."),
}


def _grp(ref=None):
    ref = ref or REFERENCE_GROUP
    return f"C(major_group, Treatment(reference='{ref}'))"


def _prep(reg):
    """Strings (not categoricals) for major_group so unused categories can't
    create all-zero columns, and a clean index for cluster-group alignment."""
    reg = reg.reset_index(drop=True).copy()
    reg["major_group"] = reg["major_group"].astype(str)
    return reg


def _fit_wls(formula, reg, weighted=True):
    """OLS with standard errors clustered by occupation (the same occupation
    appears once per source / month, so rows are not independent).
    weighted=True weights by usage share (WLS); weighted=False is plain OLS."""
    import statsmodels.formula.api as smf

    reg = _prep(reg)
    groups = pd.factorize(reg["node_name"])[0]
    if weighted:
        model = smf.wls(formula, data=reg, weights=reg["usage_pct"] + 1e-6)
    else:
        model = smf.ols(formula, data=reg)
    return model.fit(cov_type="cluster", cov_kwds={"groups": groups})


def _fit_fractional_logit(rhs, reg):
    """Fractional logit (quasi-binomial GLM) for a 0-1 outcome, UNWEIGHTED,
    with occupation-clustered standard errors (Papke-Wooldridge). It is left
    unweighted on purpose: statsmodels does not fully support clustered
    errors together with GLM weights, and it lets the comparison be clean:
        weighted WLS vs. unweighted OLS      -> effect of weighting
        unweighted OLS vs. fractional logit  -> effect of the link function
    """
    import patsy
    import statsmodels.api as sm

    reg = _prep(reg)
    y = (reg["automation_pct"] / 100).clip(1e-4, 1 - 1e-4)
    X = patsy.dmatrix(rhs, data=reg, return_type="dataframe")
    groups = pd.factorize(reg["node_name"])[0]
    model = sm.GLM(y, X, family=sm.families.Binomial())
    return model.fit(cov_type="cluster", cov_kwds={"groups": groups})


def _wald_interactions(res, prefix="source_api:"):
    """Joint test that every coefficient whose name starts with `prefix` is 0."""
    names = list(res.params.index)
    idx = [i for i, n in enumerate(names) if n.startswith(prefix)]
    R = np.zeros((len(idx), len(names)))
    for k, i in enumerate(idx):
        R[k, i] = 1.0
    w = res.wald_test(R, use_f=False)
    stat = float(np.asarray(w.statistic).ravel()[0])
    p = float(np.asarray(w.pvalue).ravel()[0])
    return stat, p, len(idx)


def _record(results, hid, estimate, p, supported, note=""):
    results.append({
        "hypothesis": hid,
        "estimate": estimate,
        "p_value": None if p is None else round(float(p), 4),
        "supported": supported,
        "note": note,
    })


def build_category_table(df, min_group_count=3):
    """One row per SOC major group: mean automation share in each source, the
    gap, and a usage-share proxy. Same construction as the category-gap and
    gap-vs-usage plots, packaged for the hypothesis tests."""
    df = add_major_group(df)
    base = df[
        (df["category_name"] == "soc_occupation")
        & (df["geo_level"] == "global")
        & (df["major_group"].notna())
    ]
    base = keep_detailed(base)

    collab = base[base["metric_id"] == "collaboration_bucket_automation_pct"]
    counts = collab.groupby(["source", "major_group"])["node_name"].nunique()
    valid = counts[counts >= min_group_count].index
    collab = collab[collab.set_index(["source", "major_group"]).index.isin(valid)]

    table = collab.pivot_table(
        index="major_group", columns="source", values="value", aggfunc="mean"
    ).dropna()
    table["gap"] = table["1P API"] - table["Claude.ai"]

    usage = base[base["metric_id"] == "pct"]
    node_usage = usage.groupby(["source", "major_group", "node_name"])["value"].mean()
    usage_total = node_usage.groupby(["source", "major_group"]).sum().groupby("major_group").mean()
    return table.join(usage_total.rename("usage_share")).dropna()


def test_h1(reg, results):
    """H1: adjusted gap > 0, and work share explains < 25% of it."""
    base_f = f"automation_pct ~ source_api + {_grp()}"
    res_a = _fit_wls(base_f, reg)                          # no work-share control
    res_b = _fit_wls(base_f + " + work_share_pct", reg)    # with work-share control

    gap_a, gap_b = res_a.params["source_api"], res_b.params["source_api"]
    lo, hi = res_b.conf_int().loc["source_api"]
    p_b = res_b.pvalues["source_api"]
    shrink = (gap_a - gap_b) / gap_a * 100 if gap_a else np.nan

    print("\n--- H1: adjusted gap and the work-share confound ---")
    print(f"Gap controlling for category only        : {gap_a:6.2f} pts")
    print(f"Gap controlling for category + work share: {gap_b:6.2f} pts "
          f"(95% CI {lo:.2f} to {hi:.2f}, p = {p_b:.4g})")
    print(f"Work share changes the gap by            : {shrink:6.1f}%")
    print(f"Work-share coefficient: {res_b.params['work_share_pct']:.3f} pts per pp "
          f"(p = {res_b.pvalues['work_share_pct']:.4g})")

    print("\nWork-share slope within each source (does the relationship differ?):")
    for src, g in reg.groupby("source"):
        r = _fit_wls(f"automation_pct ~ work_share_pct + {_grp()}", g)
        print(f"  {src:10s}: {r.params['work_share_pct']:.3f} pts per pp "
              f"(p = {r.pvalues['work_share_pct']:.4g})")

    gap_ok = bool(gap_b > 0 and lo > 0)
    mix_ok = bool(abs(shrink) < 25)
    _record(results, "H1",
            f"adjusted gap {gap_b:.1f} pts (CI {lo:.1f} to {hi:.1f}); "
            f"work share changes it by {shrink:.1f}%",
            p_b, bool(gap_ok and mix_ok),
            f"gap > 0: {gap_ok}; mix explains < 25%: {mix_ok} "
            "(model-implied, not a causal decomposition)")


def test_h2(reg, results):
    """H2: omnibus test of source x category interactions, WLS and fractional
    logit, plus Holm-adjusted per-category contrasts against the reference."""
    from statsmodels.stats.multitest import multipletests

    rhs = f"source_api * {_grp()} + work_share_pct"
    wls = _fit_wls("automation_pct ~ " + rhs, reg)
    stat_w, p_w, k = _wald_interactions(wls)

    ols = _fit_wls("automation_pct ~ " + rhs, reg, weighted=False)
    stat_o, p_o, _ = _wald_interactions(ols)

    frac = _fit_fractional_logit(rhs, reg)
    stat_f, p_f, _ = _wald_interactions(frac)

    print("\n--- H2: does the gap differ by occupation category? ---")
    print(f"Omnibus Wald test, all {k} interactions = 0 (errors clustered by occupation)")
    print(f"  WLS, usage-weighted              : chi2 = {stat_w:8.1f}, p = {p_w:.4g}")
    print(f"  OLS, unweighted                  : chi2 = {stat_o:8.1f}, p = {p_o:.4g}")
    print(f"  Fractional logit, unweighted     : chi2 = {stat_f:8.1f}, p = {p_f:.4g}")
    print("  (WLS vs OLS shows the effect of weighting; OLS vs fractional logit "
          "shows the effect of the model type.)")

    names = [n for n in wls.params.index if n.startswith("source_api:")]
    pvals = wls.pvalues[names].to_numpy()
    reject, p_adj, _, _ = multipletests(pvals, alpha=ALPHA, method="holm")
    frac_p = frac.pvalues.reindex(names)

    rows = []
    for n, b, p, pa, rj in zip(names, wls.params[names], pvals, p_adj, reject):
        label = n.split("[T.")[-1].rstrip("]")
        rows.append({"category": label, "gap_diff_vs_ref_pts": round(b, 1),
                     "p_raw": round(p, 4), "p_holm": round(pa, 4),
                     "sig_holm": bool(rj),
                     "p_fraclogit_raw": round(float(frac_p.get(n, np.nan)), 4)})
    tab = pd.DataFrame(rows).sort_values("gap_diff_vs_ref_pts", ascending=False)
    print(f"\nGap difference vs. {REFERENCE_GROUP} (WLS) with Holm correction "
          f"for {len(names)} comparisons:")
    print(tab.to_string(index=False))
    tab.to_csv(OUTPUT_DIR / "h2_category_contrasts.csv", index=False)

    _record(results, "H2",
            f"omnibus chi2 = {stat_w:.1f} (WLS), {stat_o:.1f} (OLS), {stat_f:.1f} (frac. logit)",
            max(p_w, p_o, p_f), bool(max(p_w, p_o, p_f) < ALPHA),
            f"{int(tab['sig_holm'].sum())} of {len(names)} categories differ from "
            f"{REFERENCE_GROUP} after Holm correction")


def test_h3(df, results, min_group_count=3, n_boot=2000, seed=0):
    """H3: who drives the cross-category variation in the gap?

    gap = API - Claude, so Var(gap) splits exactly into
        Cov(gap, API)/Var(gap)       = API's share, and
       -Cov(gap, Claude)/Var(gap)    = Claude.ai's share  (the two sum to 1).
    """
    t = build_category_table(df, min_group_count)
    a, c, g = t["1P API"].to_numpy(), t["Claude.ai"].to_numpy(), t["gap"].to_numpy()

    def shares(a, c):
        gap = a - c
        v = gap.var(ddof=1)
        return (np.cov(gap, a)[0, 1] / v, -np.cov(gap, c)[0, 1] / v)

    share_api, share_claude = shares(a, c)
    rng = np.random.default_rng(seed)
    boots = []
    for _ in range(n_boot):
        i = rng.integers(0, len(t), len(t))
        if (a[i] - c[i]).var(ddof=1) > 0:
            boots.append(shares(a[i], c[i])[1])
    lo, hi = np.percentile(boots, [2.5, 97.5])

    print("\n--- H3: where does the variation in the gap come from? ---")
    print(f"Across {len(t)} categories: SD of automation share  "
          f"API = {a.std(ddof=1):.1f} pts, Claude.ai = {c.std(ddof=1):.1f} pts")
    print(f"Share of gap variance from Claude.ai: {share_claude*100:.0f}% "
          f"(bootstrap 95% CI {lo*100:.0f}% to {hi*100:.0f}%); from API: {share_api*100:.0f}%")
    print("(The two shares sum to 100%; a bootstrap share can exceed 100% when the "
          "other source's share dips slightly below 0 in a resample.)")

    _record(results, "H3", f"Claude.ai share of gap variance {share_claude*100:.0f}% "
            f"(CI {lo*100:.0f}% to {hi*100:.0f}%)", None, bool(share_claude > 0.75),
            f"n = {len(t)} categories")


def plot_adjusted_gap_forest(reg):
    """One chart for the central question: the adjusted gap in each category
    with a 95% confidence interval. Intervals that clear zero (and each other)
    are what the hypothesis tests rely on; wide intervals mark thinly-used
    categories where 'no difference' really means 'not enough data'."""
    import re

    res = _fit_wls(
        "automation_pct ~ C(major_group) + C(major_group):source_api + work_share_pct", reg)
    ci = res.conf_int()
    rows = []
    for n in res.params.index:
        m = re.search(r"\[(.*)\]:source_api$", n)
        if m:
            rows.append((m.group(1), res.params[n], ci.loc[n, 0], ci.loc[n, 1]))
    t = pd.DataFrame(rows, columns=["category", "gap", "lo", "hi"]).sort_values("gap")
    t.to_csv(OUTPUT_DIR / "adjusted_gap_by_category.csv", index=False)

    fig, ax = plt.subplots(figsize=(10, 9))
    y = np.arange(len(t))
    ax.errorbar(t["gap"], y, xerr=[t["gap"] - t["lo"], t["hi"] - t["gap"]],
                fmt="o", color="#1f77b4", ecolor="#9ab9d8", capsize=3)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_yticks(y)
    ax.set_yticklabels(t["category"])
    ax.set_xlabel("Automation-share gap, 1P API minus Claude.ai (percentage points)\n"
                  "adjusted for work share; 95% CI, errors clustered by occupation")
    ax.set_title("Adjusted Automation Gap by Occupation Category")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "adjusted_gap_forest.png", dpi=300)
    plt.close()


def run_hypotheses(df):
    """Run H1-H3; one failing test never stops the others."""
    print("\n" + "=" * 70)
    print("HYPOTHESES (stated before the corrected re-run)")
    print("=" * 70)
    for hid, (claim, rule) in HYPOTHESES.items():
        print(f"{hid}: {claim}\n      Supported if: {rule}")

    reg = build_regression_dataset(df)
    print(f"\nRegression dataset: {len(reg)} source x occupation rows, "
          f"{reg['node_name'].nunique()} distinct occupations")

    results = []
    steps = [
        ("H1", lambda: test_h1(reg, results)),
        ("H2", lambda: test_h2(reg, results)),
        ("H3", lambda: test_h3(df, results)),
        ("forest plot", lambda: plot_adjusted_gap_forest(reg)),
    ]
    for name, fn in steps:
        try:
            fn()
        except Exception as e:  # keep going, report which step failed
            print(f"\n[{name}] FAILED: {type(e).__name__}: {e}")
            if name.startswith("H"):
                for hid in name.split("/"):
                    _record(results, hid, "test failed", None, None, f"{type(e).__name__}: {e}")

    summary = pd.DataFrame(results).sort_values("hypothesis")
    print("\n" + "=" * 70)
    print("HYPOTHESIS SUMMARY")
    print("=" * 70)
    print(summary.to_string(index=False))
    summary.to_csv(OUTPUT_DIR / "hypothesis_summary.csv", index=False)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = load_data()

    # Verify the structural assumptions first (months, hierarchy levels,
    # whether usage sums to ~100%) and print them so they can be checked.
    check_data_structure(df)

    plot_collaboration(df)
    plot_use_case(df)
    plot_occupation(df)
    plot_artifact_type_mix(df)
    plot_occupation_category_gap(df)
    plot_gap_vs_usage(df)
    plot_automation_work_only(df)

    print("\nProfile plots created successfully.")
    print(f"Output directory: {OUTPUT_DIR}")

    # Statistical models and hypothesis tests
    # (requires: pip install statsmodels patsy scipy)
    try:
        reg = build_regression_dataset(df)
        run_wls_model(reg)
        run_beta_model(reg)
        run_hypotheses(df)
    except ImportError as e:
        print(f"\nSkipping statistical models — missing package: {e}")
        print("Install with: pip install statsmodels patsy scipy")


if __name__ == "__main__":
    main()