# anthropic-data-science-capstone

# Consumers vs. Businesses: How Do They Use AI Differently?

Capstone project on the Anthropic Economic Index (6th release, June 26, 2026).

**Research question (Q3):** Do consumers and businesses use AI differently on the same tasks? Holding the task fixed, are companies systematically more automation-heavy than individuals, and does the gap differ by occupation category?

Consumers are proxied by **Claude.ai** traffic and businesses by **first-party (1P) API** traffic. This is a proxy, not a complete measure of either group: API traffic includes developers, Claude.ai includes people using it for work, and the API file excludes Claude Code.

> Methods, tables, and interpretation are in `Notes.md` (Steps 2-12). This README is the dated work log and a snapshot of where things stand.

---

## Repository contents

| File | Purpose |
|---|---|
| `src/inventory.py` | Inspects both CSVs and verifies the documented properties |
| `profile.py` | Builds all plots, fits the regression models, and runs the three hypothesis tests |
| `Notes.md` | Provenance, documentation summary, inventory, results, and interpretation (Steps 2-12) |
| `data/` | Raw CSVs (not tracked in git) |
| `data/profile/` | Generated plots and result tables |

## How to run

```bash
pip install pandas numpy matplotlib statsmodels patsy scipy
python src/inventory.py    # dataset inventory and verification
python profile.py          # plots, models, hypothesis tests -> data/profile/
```

Outputs in `data/profile/`: `collaboration.png`, `collaboration_work_only.png`, `use_case.png`, `artifact_type_mix.png`, `occupation_category_gap.png`, `gap_vs_usage.png`, `adjusted_gap_forest.png`, `occupation_api.png`, `occupation_claude.png`, plus `hypothesis_summary.csv`, `h2_category_contrasts.csv`, and `adjusted_gap_by_category.csv`.

---

## Work log (weekly, Monday to Sunday)

Dates come from the timestamps of working sessions and files. "Step" numbers refer to `Notes.md`.

### Week of Mon Aug 31 - Sun Sep 6, 2026
- No dated activity

### Week of Mon Sep 7 - Sun Sep 13, 2026
| Date | What was done |
|---|---|
| Mon Sep 7 | Downloaded both CSVs from Anthropic's Hugging Face repository (release `2026_06_26`). Provenance recorded (Step 2). |
| Sep 7-10  | Reviewed the report and release documentation (Step 3); ran the inventory script and verified both files (Step 4); inspected raw example rows (Step 5). |
| Thu Sep 10 | First `profile.py`: four plots (automation vs. augmentation, use-case mix, top occupations per source). First result: API 93.9% automation vs. Claude.ai 48.8%. First `profile.md` written (Step 6). |

### Week of Mon Sep 14 - Sun Sep 20, 2026
| Date | What was done |
|---|---|
| Sep 10-19  | Reviewed the plots against Q3 and found three gaps: the confound was untested, no breakdown by occupation category, nothing on what each group produces. Added the work-only control, occupation-category gap, and output-type mix. Wrote an explanation of the changes for the professor (Step 7). |
| Sat Sep 19 | Ran the revised code; five plots produced. Finding: the gap survives the work-only control. `profile.md` rewritten around the results. Next-step list drawn up (trend, usage effect, sensitivity checks, "None"/"Other" outputs, geography). |

### Weeks of Mon Sep 21, Mon Sep 28, and Mon Oct 5, 2026
- No activity recorded.

### Week of Mon Oct 12 - Sun Oct 18, 2026
| Date | What was done |
|---|---|
| Wed Oct 14, 11:13 | Redesigned the occupation-category chart as grouped bars of both sources' automation share, replacing the gap-only chart (Step 8). |
| Wed Oct 14, 11:23 | Added the gap-vs-usage scatter to test a "maturity" idea (heavier-used categories converge). |
| Wed Oct 14, 11:28 | Reviewed the scatter: r = 0.11, no relationship. Found and fixed an over-counting problem in the usage-share calculation. Chose WLS (primary) and beta regression (robustness check) as the statistical models (Step 9). |
| Wed Oct 14, 11:39 | Ran both models; shared the output. |

### Week of Mon Oct 19 - Sun Oct 25, 2026
| Date | What was done |
|---|---|
| Mon Oct 19 | Created `Notes.md` model talking points; rebuilt `profile.md` with the regression results. Shared the dataset notes (Steps 2-5) and model output for explanation. |
| Sat Oct 24, 17:02 | Asked for hypotheses. Audited the code and found that major-group (level 1) rows were being mixed with detailed occupations (level 0) in the occupation analyses. Added `DETAILED_ONLY`, `check_data_structure()`, and seven candidate hypotheses with tests. |
| Sat Oct 24, 17:10 | Narrowed to three hypotheses (H1-H3). |
| Sat Oct 24, 17:16 | Ran the corrected code on the real data. Hierarchy mix-up confirmed (44 group rows removed from the regression) but headline estimates changed by under 0.1 point. All three hypotheses supported. `Notes.md` extended with Steps 6-12; this README rewritten as a weekly log (Steps 10-11). |

---

## Results (corrected run, October 24, 2026)

| Finding | Value |
|---|---|
| Automation share, 1P API vs. Claude.ai (all traffic) | 93.9% vs. 48.8% |
| Same, work-dominant occupations only (229 occupations) | 93.7% vs. 55.0% |
| Use case: work share, API vs. Claude.ai | 83.1% vs. 44.4% |
| Adjusted gap, controlling for category | 43.2 points |
| Adjusted gap, controlling for category and work share | 38.3 points (95% CI 33.4 to 43.2) |
| How much work share changes the gap | 11.4% (about 4.9 points) |
| Gap range across 22 occupation categories | 25.9 to 47.7 points, positive in every category |
| Gap differs by category (omnibus test) | p < 1e-21 in all three model versions; 12 of 21 categories differ from Computer and Mathematical after correction |
| Claude.ai's share of the variance of the gap across categories | 125% (CI 112% to 142%); API -25% |
| Gap vs. category usage share | r = 0.13 |

| Hypothesis | Verdict |
|---|---|
| H1: firms more automation-heavy, and use-case mix does not explain it | Supported |
| H2: the gap differs by occupation category | Supported |
| H3: cross-category variation comes mainly from Claude.ai | Supported |

## Corrections log

- **Hierarchy levels were mixed** in occupation analyses until Oct 24. Fixed; the corrected run shows the effect on conclusions was negligible (Step 10).
- **"Duplicate rows" were actually two months** (April and May 2026), not duplicates. Averaging them was a valid choice, but the earlier description was wrong.
- **The usage-share measure was over-counted** twice: first by summing the two months, then by including both hierarchy levels. It is now about 93% in total, still a proxy rather than a true share of traffic.
- **The earlier beta regression was unweighted**, so its disagreements with WLS mixed the effects of weighting and model type. Step 11 separates the two.
- **The all-traffic and work-only gaps (45.1 vs. 38.7 points) are not like-for-like** (different row sets); the regression estimate (43.2 to 38.3 points) is the clean comparison.
- **`profile.md` still carries pre-correction numbers** and needs updating.

## Interpretation caveats

- Observational and aggregated: differences may reflect task, occupation, user population, product, or geography, not only business vs. consumer behavior.
- The API file excludes Claude Code, so automated coding is probably under-represented on the API side.
- Which individual categories differ depends on whether the comparison is in points or log-odds; Education is the clearest example.
- The support thresholds in H1 and H3 were set by the author before the run, not drawn from the literature.
- The two-month window cannot show a long-run trend.

## Next steps

1. Update `profile.md` with the corrected numbers.
2. Sensitivity checks: 60% work-share cutoff (try 50% and 70%), minimum occupations per category, and H3 without Education.
3. April-vs-May comparison of the gap, as a first look at change over time.
4. Pull prior Economic Index releases for the release-over-release trend.

## Citation

Massenkoff, M., Lyubich, E., Sacher, S., Hitzig, Z., Zhang, S., Heller, R., and McCrory, P. "Anthropic Economic Index report: Cadences." June 26, 2026. https://www.anthropic.com/research/economic-index-june-2026-report

---

# Activity Log

## November 2, 2026 — H1 and H2 implementation and successful full run

This entry is appended to preserve the README as it stood before this session. The earlier work log, results, hypothesis labels, corrections, caveats, and next steps above are retained as historical project documentation. The active analysis scope was subsequently narrowed to the two hypotheses described below; this update does not rewrite the earlier record.

### Code update and successful execution

- Updated `profile.py` to address the `NameError` caused by the undefined `min_group_count` variable in `plot_use_case_context()`.
- Re-ran the profiling script against the April and May 2026 Anthropic Economic Index data.
- The run completed and printed `PROFILE COMPLETE`.
- Confirmed the data contains April and May observations for both Claude.ai and 1P API.
- Confirmed occupation-level modeling uses `hierarchy_level == 0` detailed occupation rows, excluding level-1 major-group aggregates.
- Generated the current H1 and H2 plots and result tables under `data/profile/`.

### Active hypothesis scope for this phase

For the current phase of analysis, the project retains two hypotheses:

- **H1 — Output/artifact-type differences:** The distribution of reported AI output/artifact types differs between Claude.ai and first-party API usage.
- **H2 — Automation differences:** The reported automation share differs between Claude.ai and first-party API usage.

These are the H1 and H2 definitions used in the November 2 analysis. They replace the earlier H1-H3 labels only for the active analysis phase; the earlier results above remain in this README as a historical record.

### H1 — Output/artifact-type comparison

The script generated a monthly-mean comparison of reported artifact-type percentages and the 1P API minus Claude.ai percentage-point differences.

Selected results:

| Output/artifact type | 1P API (%) | Claude.ai (%) | Difference (pp) |
|---|---:|---:|---:|
| Analysis or Summary | 21.60 | 5.54 | +16.07 |
| Data or Spreadsheet | 12.99 | 3.06 | +9.94 |
| Other | 7.21 | 0.18 | +7.03 |
| Explanation or Answer | 8.08 | 16.66 | -8.58 |
| Document or Report | 5.80 | 14.66 | -8.87 |
| Advice or Recommendation | 2.00 | 10.39 | -8.39 |

The output also includes a `None` category (15.86% for 1P API and 6.79% for Claude.ai). This category is retained pending a denominator and missing-category audit; it should not be interpreted as a substantive artifact type.

H1 is currently treated as a descriptive comparison. The current analysis does not calculate a chi-square test or p-value from aggregate percentages without the underlying category counts and sampling uncertainty.

### H2 — Automation versus augmentation

Overall monthly-mean collaboration split:

| Source | Augmentation (%) | Automation (%) |
|---|---:|---:|
| Claude.ai | 51.20 | 48.80 |
| 1P API | 6.06 | 93.94 |

Work-dominant occupation comparison (229 matched detailed occupations; at least 60% work share in both sources):

| Source | Augmentation (%) | Automation (%) |
|---|---:|---:|
| Claude.ai | 45.04 | 54.96 |
| 1P API | 6.32 | 93.68 |

Occupation-adjusted model output:

- Regression observations: 1,413 source-by-occupation observations.
- Distinct detailed occupations: 744.
- Automation-share difference adjusted for occupation major group: 43.21 percentage points.
- Difference adjusted for occupation major group and work-use share: 38.30 percentage points.
- 95% confidence interval for the fully adjusted WLS estimate: 33.40 to 43.19 percentage points.
- WLS p-value: 4.32e-53.
- The coefficient attenuated by 11.4% after adding work-use share to the occupation-adjusted model.

Robustness checks with the same adjusted covariates reported the same positive direction:

- WLS with usage-share proxy weights and occupation-clustered standard errors: p = 4.32e-53.
- Unweighted OLS with occupation-clustered standard errors: the console displayed `p = 0`; this is a numerical display/precision issue, not a literal zero p-value.
- Fractional logit with clustered standard errors: the console displayed `p = 0`; this is a numerical display/precision issue, not a literal zero p-value.

The 11.4% figure is coefficient attenuation after adding work-use share. It is not a causal decomposition and should not be described as the percentage of the gap causally explained by work-use share. The analysis is observational and uses aggregate release data. The `pct` weighting variable is a usage-share proxy, not a raw sample size.

### Generated plots

The successful run generated:

- `h1_output_type_mix.png`
- `h2_collaboration_overall.png`
- `h2_work_dominant_occupations.png`
- `use_case_context.png`

### Follow-up fixes and methodological audit

The November 2 run establishes a successful execution baseline. The results still require methodological and presentation checks before they are treated as final.

1. **H1 denominator and missing-category audit:** Determine what `None` represents and verify whether artifact percentages use comparable denominators across sources.
2. **Monthly averaging validation:** Verify that taking the arithmetic mean of April and May percentages is appropriate for each metric and source.
3. **H2 model audit:** Review the regression specification, WLS weighting, occupation-clustered standard errors, and interpretation of the coefficient in percentage points.
4. **P-value formatting:** Display very small p-values in scientific notation rather than rounding them to zero.
5. **Plot presentation:** Improve figure dimensions, title wrapping, label readability, and layout so titles and legends are not clipped.

No additional hypotheses were introduced in the November 2 session. The active scope remains H1 (output/artifact-type distribution differences) and H2 (automation-share differences).
