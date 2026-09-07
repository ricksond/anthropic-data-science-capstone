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

The raw CSV files are stored locally in the project's `data/` directory and are excluded from git tracking. The repository will contain scripts used to inspect and process the data rather than the raw dataset itself.