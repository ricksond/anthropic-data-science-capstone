# Dataset Notes

## Step 2 : Data Provenance

## Dataset

**Anthropic Economic Index - 6th release (June 26, 2026)**

The project uses the June 26, 2026 release of the Anthropic Economic Index, which contains updated analysis of AI usage across real world economic tasks, including Claude.ai and first party API data.

### Primary Source

The dataset was obtained directly from Anthropic's Official Hugging Face dataset repository:

https://huggingface.co/datasets/Anthropic/EconomicIndex

The specific release used in this project is:

https://huggingface.co/datasets/Anthropic/EconomicIndex/tree/main/release_2026_06_26

The data files are located under data directory:

https://huggingface.co/datasets/Anthropic/EconomicIndex/tree/main/release_2026_06_26/data

### Files Used

- `aei_claude_ai_2026-06-26.csv`
- `aei_1p_api_2026-06-26.csv`

These are the two data files provided in the June 26,2026 Release.


### Version / Release

**Release:** `release_2026_06_26`

**Release Date:** June 26, 2026

This is the sixth release of the Anthropic Economic Index

### Download Date

**September 7th, 2026**

### License

The Anthropic documentation states that the **data are released under
CC-BY**. The code associated with this project is the MIT License and hence this project will be treated as
**CC-BY licensed data**

### Citations Requested by the authors

 - Massenkoff, Maxim, Eva Lyubich, Szymon Sacher, Zoe Hitzig, Shaoyi Zhang,
 - Ryan Heller, and Peter McCrory. "Anthropic Economic Index report:
 - Cadences." June 26, 2026.

 BibTeX:

@online{anthropic2026aeiv6,
    author = {Maxim Massenkoff and Eva Lyubich and Szymon Sacher and Zoe Hitzig and Shaoyi Zhang and Ryan Heller and Peter McCrory},
    title = {Anthropic Economic Index report: Cadences},
    date = {2026-06-26},
    year = {2026},
    url = {https://www.anthropic.com/research/economic-index-june-2026-report},
}

### Provenance Statement

The raw data in this project were obtained directly from Anthropic's official Economic Index repository on Hugging face rather than from a mirror or another student's copy. This project uses the most recent available release at the time of data acquisation, `release_2026_06_26`

The raw CSV files are stored locally in the project's `data/` directory and are excluded from git tracking. The repository will contain scripts used to inspect and process the data rather than the raw dataset.


## Step 3: Dataset Documentation and Paper Summary

### Primary Documentation

The Primary documentation for this project is the June 26, 2026 Antrhopic Economic Index report, "Cadences", and the release-specific data documentation for `release_2026_06_26`.

Report:

https://www.anthropic.com/research/economic-index-june-2026-report

Release Documentation:
https://huggingface.co/datasets/Anthropic/EconomicIndex/blob/main/release_2026_06_26/data_documentation.md

The previously releases 2025 Economic Index paper was laso reviewed as methodological background. It documents the development of the O*NET task mapping and the five collaboration-pattern classifications. However, the 2026 report and release documentation are treated as the authoritative sources for the data analyzed in this project.

### How the Data were collected

Anthropic uses privacy-preserving classifiers to analyze sampled Claude usage. The June 26,2026 report describes chages to the Economic Index pipeline, including higher frequency sampling, a new classfier for conversation outputs, and more granular reporting of claude conversations and first party API usage.

The release data used in this project are aggregated at hte calendar-month level and cover months April and May 2026.

The release contains two source files:

1. `aei_claude_ai_2026-06-26.csv`
   - Claude chat and Coworks and Free, Pro, and Max accounts
   - Includes Claude.ai and the Claude desktop application
   - Global, country, and subregion breakdowns

2. `aei_1p_api_2026-06-26.csv`
   - Anthropic first-party API traffic
   - Excludes Claude Code
   - Global-level data only

### Unit of Observation

A roaw doesn't represent an individual user, business , conversation or task.

According to the release documentation, each row represents one published metric value for a specific geography and category combination.

Important dimensions are as follows:

- `date_start`
- `date_end`
- `geo_id`
- `geo_level`
- `category_name`
- `hierarchy_level`
- `metric_id`
- `value`
- `node_name`
- `node_external_id`

### Task and occupation classifications

The release provided several analysis categories. the `onet` category represents work activities from the U.S Department of Labor O*NET database:

- Level 0: Task
- Level 1: Detailed Work Activity
- Level 2: Intermediate Work Activity
- Level 3: Generalized Work Activity

The `soc_occupation` category represents occupations from the U.S Bureau of Labor Statistics Standaed Occupational Classification:

- Level 0: Detailed Occupation
- Level 1: Major Group

### Collaboration labels

The methodologu identifies 5 collaboration patterns:

-Directive
-Feedback Loop
-Task Iteration
-Learning
-Validation

The 2025 Methodology paper reported 90.7% optimal agreement in Human validation of 150 conversations. This is methodological background, not a verification target for the 2026 CSVs.

### Verification Targets for Step 4

The Inventory scripts will verify:
1. Data covers April and May 2026.
2. the release contains:
    `aei_claude_ai_2026-06-26.csv`
    `aei_1p_api_2026-06-26.csv`
3. Published file sizes are approximately 219MD and 77.3MB

4. Claude.ai includes global, country and subregion data; 1P API is global only.

5. Both Sources contain O*NET, request, and SOC classifications globally.

### Relevance to Research Question Q3

This project compares Claude.ai as a consumer-facing souces with 1P API as a business/developer-oriented source. This is a proxy, not a complete measure of all consumers or businesses.

Because the data are observational and aggregated, differences may reflect task,occupation,user population,product or geographic composition. The analysis will therefore compare overall differences and differences within comparable tasks and occupations.

## Step 4: Dataset Inventory and Verification

The inventory script src/inventory.py was used to inspect both release csv files and verify the targets documented in Step 3


                                             Claimed vs. Actual
|       Target	           |           Claimed	          |      Actual	                |  Result      |
| :--------------------:   | :-------------------------:  |  :----------------------:   | :----------: |
|  Release period	       | April–May 2026	              |  April–May 2026	            |    PASS      |
|  Claude geography	       | Global, country, subregion	  |  Global, country, subregion |	 PASS      |
|  1P API geography	       | Global only	              |  Global only	            |    PASS      |
|  Claude categories	   | Overall, O*NET, request, SOC |	 All four present	        |    PASS      |
|  1P API categories	   | Overall, O*NET, request, SOC |	 All four present	        |    PASS      |
|  Claude missing values   | No missing values expected	  |  0% across all columns	    |    PASS      |
|  1P API missing values   | No missing values expected	  |  0% across all columns	    |    PASS      |
|  Claude columns	       | 10 documented fields	      |          10                 |    PASS      |
|  1P API columns	       | 10 documented fields		  |          10                 |    PASS      |

### Dataset Inventory
- Claude.ai: 1,636,573 rows, 10 columns, 209.02 MB
- 1P API: 491,705 rows, 10 columns, 73.70 MB
- Both files contain the documented fields: date_start, date_end, geo_id, geo_level, category_name, hierarchy_level, metric_id,       value, node_name, and node_external_id.
- All columns have a 0.00% missing-value rate in both files. 
- The inventory script confirmed all Step 3 verification targets with no failures.

## Step 5: Raw Example Inspection

The inventory Script selected five examples from each CSV to inspect the data structure and meaning of individual observations.

|Source	    |   Date	  |        Geography	            |   Category	    |  Metric	                             |    Value	|
|:--------: | :--------:  | :-----------------------------: | :---------------: | :------------------------------------: | :------: |
|Claude.ai	| May 2026	  |  Western Cape, South Africa	    |  O*NET	        |  pct	                                 |    0.25	|
|Claude.ai	| May 2026	  |  Cameroon	                    |  Request	        |  pct	                                 |    0.89	|
|Claude.ai	| April 2026  |  Philippines	                |  O*NET	        |  pct	                                 |    0.09	|
|Claude.ai	| May 2026	  | Argentina (Buenos Aires)        |  SOC occupation   |  pct	                                 |    0.83	|
|Claude.ai	| May 2026	  | Global	                        |  SOC occupation	|  use_case_work_pct	                 |    42.60 |
|1P API	    | May 2026	  | Global	                        |  O*NET	        |  use_case_personal_pct	             |    2.67  |
|1P API	    | May 2026	  | Global	                        |  O*NET	        |  artifact_translation_pct	             |    0.19  |
|1P API	    | May 2026	  | Global	                        |  O*NET	        |  artifact_advice_or_recommendation_pct |	  0.00	|
|1P API	    | May 2026	  | Global	                        |  SOC occupation	|  human_only_ability_pct	             |	  95.20 |
|1P API	    | April 2026  |   Global	                    |  Request	        |  pct	                                 |     0.75 |

### Observations

The examples show that each row represents an aggregated metric for a specific time period,
geography,category, and task or occupation. The metric_id determines what the reported value measures, while 
node_name and node_external_id identify the associated task, request or occupation.

The examples also show that Claude.ai contains geographic variation, while the 1P API examples are global. Values cannot be interpreted without considering the metric being reported; for example, 0.25 for pct and 42.60 for use_case_work_pct represent different measures.



## Step 6: First Profile Plots (September 10, 2026)

`profile.py` loads both CSVs, labels each with a `source` (Claude.ai or 1P API), keeps global-level rows, and plots four views.

| Measure | 1P API | Claude.ai |
| :--: | :--: | :--: |
| Automation share | 93.9% | 48.8% |
| Augmentation share | 6.1% | 51.2% |
| Work use case | 83.1% | 44.4% |
| Personal use case | 14.2% | 39.3% |
| Coursework use case | 2.7% | 16.2% |

The top-10 occupation charts put Computer and Mathematical first in both sources (about 28% of API usage and 24% of Claude.ai usage).

### What this first pass could not show
- It showed that a gap exists, but not whether the gap is real or a side effect of the two sources doing different kinds of work (83% work use vs. 44%).
- It had no occupation-level automation comparison, which is the second half of Q3.
- Nothing described *what* each group produces with AI.

## Step 7: Refocusing the Plots on Q3 (September 10-19, 2026)

Three analyses were added so each plot answers part of the research question.

| Addition | Question it answers | Method |
| :--: | :--: | :--: |
| Work-only control | Is the gap just "work tasks are more automatable"? | Keep occupations that are at least 60% work use in both sources; usage-weighted automation share |
| Occupation-category gap | Does the gap differ by category? | Roll detailed occupations up to the 22 SOC major groups with enough data, using the first two digits of the SOC code |
| Output-type mix | What do the two groups actually produce? | Compare the `artifact_*_pct` metrics between sources |

### Work-only control (final numbers)
229 occupations are at least 60% work use in both sources.

| Source | Automation | Augmentation |
| :--: | :--: | :--: |
| 1P API | 93.7% | 6.3% |
| Claude.ai | 55.0% | 45.0% |

The API figure barely moves from the all-traffic result. The all-traffic numbers come from the `overall` rows and the work-only numbers from occupation rows, so the two gaps (45.1 vs. 38.7 points) are not directly comparable; the regression in Step 11 gives the like-for-like estimate of how much work share matters.

### Automation share by occupation category (final numbers)

| Category | 1P API | Claude.ai | Gap (pts) |
| :-- | :--: | :--: | :--: |
| Arts, Design, Entertainment, Sports, and Media | 91.9 | 44.3 | 47.7 |
| Sales and Related | 91.9 | 45.6 | 46.3 |
| Business and Financial Operations | 93.7 | 48.0 | 45.7 |
| Life, Physical, and Social Science | 89.4 | 43.9 | 45.5 |
| Management | 93.9 | 48.8 | 45.0 |
| Legal | 87.3 | 42.3 | 45.0 |
| Community and Social Service | 88.6 | 45.1 | 43.6 |
| Healthcare Practitioners and Technical | 92.1 | 48.6 | 43.5 |
| Architecture and Engineering | 90.1 | 48.0 | 42.0 |
| Construction and Extraction | 94.5 | 54.4 | 40.1 |
| Educational Instruction and Library | 74.7 | 35.1 | 39.6 |
| Personal Care and Service | 94.4 | 57.0 | 37.4 |
| Healthcare Support | 94.6 | 57.3 | 37.3 |
| Protective Service | 96.6 | 60.1 | 36.6 |
| Office and Administrative Support | 95.9 | 60.0 | 35.9 |
| Food Preparation and Serving Related | 92.5 | 57.3 | 35.1 |
| Building and Grounds Cleaning and Maintenance | 94.4 | 60.8 | 33.6 |
| Computer and Mathematical | 93.3 | 61.1 | 32.2 |
| Transportation and Material Moving | 96.3 | 65.1 | 31.2 |
| Production | 94.6 | 65.5 | 29.1 |
| Installation, Maintenance, and Repair | 95.9 | 67.3 | 28.5 |
| Farming, Fishing, and Forestry | 93.3 | 67.4 | 25.9 |

The gap is positive in all 22 categories and ranges from 25.9 to 47.7 points. API automation is high almost everywhere (87-97%, with Education at 74.7% the clear low point); most of the variation in the gap comes from how collaboratively individuals use Claude.ai (35% to 67% automation).

### Output types (top 12 by largest share, % of traffic)

| Output type | 1P API | Claude.ai |
| :-- | :--: | :--: |
| Analysis or Summary | 21.6 | 5.5 |
| None | 15.9 | 6.8 |
| Data or Spreadsheet | 13.0 | 3.1 |
| Explanation or Answer | 8.1 | 16.7 |
| Other | 7.2 | 0.2 |
| Document or Report | 5.8 | 14.7 |
| Code Fix or Debug | 4.8 | 3.5 |
| Advice or Recommendation | 2.0 | 10.4 |
| Email or Message | 2.3 | 4.6 |
| App or Website | 2.4 | 4.2 |
| Plan or Strategy | 0.9 | 4.0 |
| Script or Snippet | 1.9 | 3.2 |

Businesses concentrate on analysis, summaries, and structured data work. Individuals concentrate on explanations, documents, and advice. About 23% of API traffic falls in "None" or "Other", which limits how precisely that side can be described.

## Step 8: Chart Redesign and Usage Check (October 14, 2026)

### Category chart redesign
The gap-only bar chart could not distinguish "95% vs. 50%" from "60% vs. 15%" (same gap, different story), and its red/blue coloring by sign carried no information because every gap is positive. It was replaced with grouped bars of both sources' automation share, sorted by gap, with the gap labeled on each row.

### Does heavier usage mean a smaller gap?
Computer and Mathematical is the most-used category and has one of the smaller gaps, which suggested a "maturity" story. A scatter plot of gap vs. category usage share tests this.

| Run | Pearson r |
| :--: | :--: |
| First run (before the level fix in Step 10) | 0.11 |
| Final run (level-0 occupations only) | 0.13 |

Both are close to zero, so there is no evidence that usage volume explains the gap. Computer and Mathematical is still a high-leverage point (usage share 25.8 vs. 12.9 for the next category), so this means "no evidence of a relationship," not "proven none."

## Step 9: Statistical Models (October 14, 2026)

The charts describe patterns; they cannot say whether a difference is larger than noise. Two regressions were fit on one row per source x occupation, with automation share as the outcome:

`automation_pct ~ source x occupation category + work share`

| Term | What it means |
| :--: | :-- |
| `source_api` | The automation gap (API minus Claude.ai) in the reference category (Computer and Mathematical), holding work share fixed |
| `source_api x category` | How much another category's gap differs from the reference category's gap |
| `work_share_pct` | The use-case confound control: points of automation per point of work share |

### Weighted least squares (WLS), the primary model
Ordinary regression finds the straight-line relationship between predictors and an outcome. The weighted version lets occupations with more traffic count more, which matters because the file reports percentages without sample sizes, so usage share is the best available stand-in for how much to trust each occupation's number. Coefficients are in percentage points, which makes it easy to explain.

### Beta regression, the robustness check
Automation share is a percentage capped at 100%, and the API sits near that ceiling (about 94%). A straight-line model can in principle predict above 100% and handles errors poorly near the cap. Beta regression is built for bounded proportions and works on the log-odds scale, where differences near the ceiling are stretched out. If both models agree, the finding does not depend on the straight-line assumption.

### Results (level-0 occupations, 1,413 rows)

| Estimate | WLS (points) | Beta (log-odds) |
| :--: | :--: | :--: |
| API vs. Claude.ai, reference category | +25.9 (p < 0.001) | +1.69 (p < 0.001), odds ratio about 5.4 |
| Work share, per +1 point | +0.136 (p < 0.001) | +0.0075 (p < 0.001) |
| R-squared / precision | 0.900 | precision 2.55 |

These tables print ordinary standard errors. Step 11 repeats the key tests with errors clustered by occupation, which is the more trustworthy version.

## Step 10: Data-Structure Audit (October 24, 2026)

### What triggered it
The top-10 occupation charts listed major-group names ("Computer and Mathematical", "Management") next to individual jobs. Step 3 of these notes records that `soc_occupation` has two levels (0 = detailed occupation, 1 = major group), so the group totals were being treated as occupations. `check_data_structure()` was added to `profile.py` to verify this instead of assuming it.

### What the check showed

| Check | Result |
| :-- | :-- |
| Months present | April and May 2026 in both sources (the "repeated" rows per occupation are two different months, not duplicates) |
| SOC rows, level 0 / level 1 | 1P API: 68,532 / 2,142; Claude.ai: 72,107 / 2,244 |
| Level 0 examples | Heating, Air Conditioning, and Refrigeration Mechanics and Installers; Financial Quantitative Analysts; Urban and Regional Planners |
| Level 1 examples | Personal Care and Service; Computer and Mathematical; Farming, Fishing, and Forestry |
| `pct` summed over level 0, per source-month | 87.3 to 98.5 |
| `pct` summed over level 1, per source-month | 88.5 to 98.7 |

Each level adds up to roughly 90-99%, so summing both together gave about 190% (the "usage share" over 100% seen earlier). The reason the sums are somewhat below 100% was not investigated.

### The fix and its effect
`DETAILED_ONLY = True` keeps level-0 rows in every occupation analysis. The regression went from 1,457 to 1,413 rows, exactly the 44 group rows removed (22 categories x 2 sources).

| Quantity | Before (levels mixed) | After (level 0 only) |
| :-- | :--: | :--: |
| WLS gap, reference category | +26.00 | +25.93 |
| WLS work-share coefficient | 0.1357 | 0.1356 |
| Beta gap (log-odds) | 1.697 | 1.695 |
| WLS R-squared | 0.947 | 0.900 |
| Gap range across categories | 27.5-48.0 | 25.9-47.7 |
| Work-only matched occupations | 232 | 229 |
| Work-only Claude.ai automation | 53.1% | 55.0% |
| Gap vs. usage correlation | 0.11 | 0.13 |

The conclusions did not change. The main visible difference is the lower R-squared: the group rows carried the heaviest weights and were easy to fit.

## Step 11: Hypotheses and Results (October 24, 2026)

Three hypotheses were written down with a support rule before the corrected run, so the verdicts could not be fitted afterwards. Tests use errors clustered by occupation (the same occupation appears in both sources).

| # | Hypothesis | Support rule | Result |
| :--: | :-- | :-- | :-- |
| H1 | Firms are more automation-heavy, and the use-case mix does not explain it | Adjusted gap > 0 with a 95% CI excluding 0, and work share shrinks the gap by < 25% | **Supported** |
| H2 | The gap differs by occupation category | Omnibus test rejects in weighted WLS, unweighted OLS, and unweighted fractional logit | **Supported** |
| H3 | Cross-category variation in the gap comes mainly from Claude.ai | Claude.ai accounts for > 75% of the gap's variance | **Supported** |

### H1: the gap is large and mostly survives the work-share control

| Quantity | Value |
| :-- | :--: |
| Gap controlling for category only | 43.2 points |
| Gap controlling for category + work share | 38.3 points (95% CI 33.4 to 43.2, p < 0.001) |
| Change from adding work share | 11.4% (about 4.9 points) |
| Work-share slope, API | 0.130 points per point (p < 0.001) |
| Work-share slope, Claude.ai | 0.138 points per point (p = 0.008) |

The work/personal mix explains roughly a tenth of the gap. The similar slopes in the two sources suggest the control behaves consistently. This is a model-implied estimate: the 39-point work-share difference between sources times 0.137 is about 5.3 points, close to the observed 4.9.

### H2: the gap differs by category, though which categories stand out depends on the model

Joint test that all 21 source x category interactions are zero:

| Model | Chi-square | p |
| :-- | :--: | :--: |
| WLS, usage-weighted | 161.2 | 1.3e-23 |
| OLS, unweighted | 153.9 | 3.2e-22 |
| Fractional logit, unweighted | 204.8 | 4.1e-32 |

All three reject. Comparing WLS with OLS shows the effect of weighting; comparing OLS with fractional logit shows the effect of the model type. Neither changes the verdict.

Per-category gap difference versus Computer and Mathematical (WLS, Holm-corrected for 21 comparisons; fractional-logit p is uncorrected):

| Category | Gap difference (pts) | Holm significant | Fractional-logit p |
| :-- | :--: | :--: | :--: |
| Arts, Design, Entertainment, Sports, and Media | +29.5 | Yes | 0.006 |
| Management | +21.4 | Yes | 0.0001 |
| Healthcare Support | +21.0 | Yes | 0.19 |
| Business and Financial Operations | +20.9 | Yes | 0.0002 |
| Legal | +20.9 | Yes | 0.74 |
| Life, Physical, and Social Science | +20.2 | Yes | 0.48 |
| Educational Instruction and Library | +15.9 | Yes | 0.0001 |
| Architecture and Engineering | +15.5 | Yes | 0.62 |
| Healthcare Practitioners and Technical | +14.8 | Yes | 0.20 |
| Transportation and Material Moving | +14.3 | Yes | 0.016 |
| Sales and Related | +14.3 | Yes | 0.16 |
| Community and Social Service | +14.2 | Yes | 0.91 |
| Building and Grounds Cleaning and Maintenance | +13.7 | No | 0.75 |
| Food Preparation and Serving Related | +9.3 | No | 0.63 |
| Office and Administrative Support | +7.2 | No | 0.003 |
| Personal Care and Service | +5.5 | No | 0.19 |
| Farming, Fishing, and Forestry | +3.1 | No | 0.33 |
| Production | +0.4 | No | 0.97 |
| Construction and Extraction | -1.6 | No | 0.049 |
| Installation, Maintenance, and Repair | -3.4 | No | 0.41 |
| Protective Service | -7.9 | No | 0.001 |

Reading this honestly:
- Twelve of 21 categories differ from Computer and Mathematical under WLS after correction.
- The categories that stand out in both models, with the same direction, are Arts/Media, Management, Business and Financial, and Transportation.
- Education is significant in both but the direction depends on the scale. In percentage points its gap (39.6) is larger than Computer and Mathematical's (32.2), but on the log-odds scale it is smaller (about 1.7 vs. 2.2, calculated from the category means), because its API automation is unusually low (74.7%).
- Several categories are significant only in one model (for example Legal and Healthcare Support in WLS; Protective Service and Office in the fractional logit). The categories with the smallest gaps (Farming, Production, Installation, Construction) are low-usage, so their wide intervals mean "not enough data," not "no difference."

### H3: Claude.ai drives the cross-category variation

| Quantity | Value |
| :-- | :--: |
| Spread of automation share across 22 categories | API 4.7 points, Claude.ai 9.2 points |
| Share of gap variance from Claude.ai | 125% (bootstrap 95% CI 112% to 142%) |
| Share of gap variance from the API | -25% |

The two shares always sum to 100%. A share above 100% with a negative API share means the gap is *smaller* where the API automates *more*, which can only happen if the two sources' automation levels rise and fall together across categories (their correlation must exceed about 0.5, the ratio of the two spreads). In plain terms: categories where individuals work most collaboratively are also, somewhat, categories where firms automate less, but the individual side varies about twice as much. The rule is met, but "firms automate uniformly" is too strong: the API spread of 4.7 points is not zero, and Education (74.7%) is its clear low point.

## Step 12: Limitations and Next Steps

### Limitations
- **Proxy groups:** Claude.ai and the API stand in for consumers and businesses. API traffic includes developers, Claude.ai includes work use, and the API file excludes Claude Code, so automated coding is probably under-represented on the API side.
- **Observational and aggregated:** differences may reflect task, occupation, user population, product, or geography, not only business-vs-consumer behavior.
- **Weights are a proxy:** usage share stands in for sample size, which the file does not provide.
- **Scale dependence:** which individual categories look different depends on whether the comparison is in points or log-odds.
- **Two adjacent months:** the release cannot show a long-run trend.
- **Rules were mine:** the support thresholds (25%, 75%) were chosen by me before the run, not taken from the literature.

### Next steps
1. Update `profile.md` with the corrected numbers (it still carries the earlier mixed-level figures).
2. Sensitivity checks: the 60% work-share cutoff (try 50% and 70%), the minimum occupations per category, and H3 with Education excluded.
3. April-vs-May comparison of the gap, as a first look at change over time.
4. Pull prior Economic Index releases to study the release-over-release trend, which remains the unstudied part of Q3.