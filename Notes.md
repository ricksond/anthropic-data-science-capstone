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
|:--------------------------------------------------------------------------------------------------:  |
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


