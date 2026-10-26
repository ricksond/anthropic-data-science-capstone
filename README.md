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