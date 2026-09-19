# Consumer vs. Enterprise AI Usage: A Comparative Profile

**Research Question (Q3):** Do consumers and businesses use AI differently on the same tasks? Holding tasks fixed and comparing Claude.ai (largely consumer/prosumer traffic) against the 1P (first-party) API (largely enterprise/developer-integrated traffic): Are companies systematically more automation-heavy than individuals? Does the gap differ by occupation category?

**Data source:** Anthropic Economic Index, release `2026_06_26`
(https://huggingface.co/datasets/Anthropic/EconomicIndex/tree/main/release_2026_06_26/data)
- `aei_claude_ai_2026-06-26.csv` — 1,636,573 rows, Claude.ai traffic
- `aei_1p_api_2026-06-26.csv` — 491,705 rows, 1P API traffic

Both files share a schema (`date_start`, `date_end`, `geo_id`, `geo_level`, `category_name`, `hierarchy_level`, `metric_id`, `value`, `node_name`, `node_external_id`) and cover the same month (2026-04-01/05-01 → 2026-05-01/06-01).

---

## 1. Headline result: businesses are far more automation-heavy — and it's not a task-mix artifact

![Automation vs Augmentation, all traffic](collaboration.png)

| Source | Automation % | Augmentation % |
|---|---|---|
| 1P API | 93.9% | 6.1% |
| Claude.ai | 48.8% | 51.2% |

Unadjusted, the 1P API is almost entirely automation-coded (94%), while Claude.ai is close to an even split. The obvious objection: 1P API traffic is 83% "work" use case vs. only 44% for Claude.ai (see §3), so maybe this gap is just "work tasks are more automatable," not a real business-vs-individual difference.

**We tested this directly, and the confound does not explain the gap.**

![Automation vs Augmentation, work-only, usage-weighted](collaboration_work_only.png)

Restricting the comparison to occupations that are ≥60% work-use-case in *both* sources, usage-weighted:

| Source | Automation % | Augmentation % |
|---|---|---|
| 1P API | 93.9% | 6.1% |
| Claude.ai | 53.1% | 46.9% |

The 1P API's split is **identical** to the unadjusted figure. Claude.ai's automation share actually rises slightly (48.8% → 53.1%) once restricted to work-dominant occupations, rather than falling toward the API's number as the confound hypothesis would predict. **This is the key finding: the ~45-point automation gap is not an artifact of businesses doing more automatable tasks. It survives, essentially unchanged, when the task-type mix is held fixed.** The gap reflects a genuine difference in *how* the same kind of task is handled — API integrations are built for unattended, single-shot completion, while Claude.ai sessions retain an interactive human reviewer by construction.

## 2. The gap holds in every single occupation category, but its size varies 1.8x

![Automation gap by occupation category](occupation_category_gap.png)

Rolling ~800 detailed occupations up into their 23 SOC major groups and computing the automation-share gap (1P API − Claude.ai) within each:

| Rank | Category | Gap (points) |
|---|---|---|
| Largest | Arts, Design, Entertainment, Sports, and Media | ~48 |
| | Sales and Related | ~46 |
| | Business and Financial Operations | ~45 |
| | Legal | ~45 |
| | Life, Physical, and Social Science | ~45 |
| | Management | ~44 |
| ⋯ | ⋯ | ⋯ |
| | Computer and Mathematical | ~32 |
| | Transportation and Material Moving | ~31 |
| | Production | ~29 |
| | Installation, Maintenance, and Repair | ~28 |
| Smallest | Farming, Fishing, and Forestry | ~27 |

Two things worth flagging:

1. **Every category shows a positive gap** (1P API more automation-heavy than Claude.ai in all 23 groups) — the effect is directionally universal, not concentrated in one or two categories.
2. **But the effect size is not uniform** — it ranges from ~27 to ~48 points, a ~1.8x spread. Notably, **Computer and Mathematical** — the single largest occupation category by usage in both sources (see §3) — has one of the *smaller* gaps. This suggests that for core technical/coding work specifically, business and individual usage patterns converge more than they do for creative, sales, legal, or scientific work, where the gap is largest. That's a substantive, occupation-specific claim the unadjusted overall comparison could never have surfaced.

## 3. What are they actually doing? Use case and output type

![AI Use by Use Case](use_case.png)

| Source | Work % | Personal % | Coursework % |
|---|---|---|---|
| 1P API | 83.1% | 14.2% | 2.7% |
| Claude.ai | 44.4% | 39.3% | 16.2% |

This confirms the confound tested (and ruled out) in §1: the API is overwhelmingly work-oriented; Claude.ai spans work, personal, and coursework fairly evenly.

![Top output types, businesses vs individuals](artifact_type_mix.png)

Beyond *how automated* the interaction is, the two populations produce visibly different *kinds* of output:

| Output type | 1P API | Claude.ai | Skews toward |
|---|---|---|---|
| Analysis or Summary | ~21.5% | ~5.5% | **Business** |
| Data or Spreadsheet | ~13% | ~3% | **Business** |
| "None" (no clear artifact) | ~16% | ~7% | **Business** |
| Other | ~7% | ~0.3% | **Business** |
| Code Fix or Debug | ~5% | ~3.5% | Business (slight) |
| Explanation or Answer | ~8% | ~17% | **Individual** |
| Document or Report | ~6% | ~14.5% | **Individual** |
| Advice or Recommendation | ~2% | ~10.5% | **Individual** |
| Plan or Strategy | ~1% | ~4% | **Individual** |
| Email or Message | ~2.3% | ~4.7% | Individual (slight) |
| App or Website | ~2.3% | ~4.2% | Individual (slight) |
| Script or Snippet | ~2% | ~3.2% | Individual (slight) |

Businesses concentrate on **bulk analytical and structured-data processing** (analysis/summary, spreadsheets) — the kind of repeatable, high-volume work that's easy to hand off completely, consistent with the automation split in §1. Individuals concentrate on **advisory and communicative** outputs (explanations, advice, documents, plans) — work that benefits from an iterative back-and-forth, consistent with their near-even automation/augmentation split.

## 4. Answering Q3

**Are companies systematically more automation-heavy than individuals, on the same tasks?**
Yes, and the effect is robust: the ~45-point automation gap survives essentially unchanged after controlling for the work/personal/coursework mix difference between the two channels (§1). This is not merely a byproduct of businesses doing more inherently automatable tasks — it reflects a real difference in interaction style between embedded/pipeline API usage and supervised conversational usage.

**Does the gap differ by occupation category?**
Yes, but the direction is universal — every one of the 23 SOC major groups shows a positive automation gap, so there is no occupation category where individuals are *more* automation-heavy than businesses. The *magnitude* varies meaningfully (27–48 points), and is smallest in Computer and Mathematical work — the category both populations use most — and largest in creative, sales, legal, and scientific categories.

**What this adds to the "will firms automate faster than workers augment?" debate:**
The evidence here says yes, firms are automating faster, and it isn't just because they're pointed at easier tasks — the effect persists within matched task types and matched occupation categories. But the convergence in Computer and Mathematical work is a genuinely interesting exception worth further investigation: it may indicate that as a task category matures in both consumer and enterprise usage, the automation gap compresses.

## 5. Remaining limitations

- **Single release, no trend:** this uses one Economic Index release (`2026_06_26`). The research question's core interest in the *release-over-release trend* in the automation gap remains untested — that requires pulling and re-running this pipeline against prior releases with `date_start`/`date_end` as a grouping variable.
- **Occupation-category aggregation is a proxy:** rolling detailed SOC occupations up via the first two digits of `node_external_id` is standard SOC structure, but categories with `min_group_count < 3` detailed occupations in either source were dropped to avoid single-occupation noise standing in for an entire category — check the console output from `plot_occupation_category_gap` for exactly which categories were excluded.
- **`work_threshold=60%` is a judgment call:** the work-only control in §1 used a 60% work-share cutoff for "work-dominant." It would strengthen the finding to show it's not sensitive to this choice (e.g. also report 50% and 70% cutoffs).
- **"None" and "Other" artifact categories (§3):** a combined ~20%+ of 1P API traffic falls into these uninformative buckets, which limits how precisely the output-type comparison characterizes actual business API usage — likely reflects programmatic/classification-style API calls that don't map cleanly onto the artifact taxonomy built around conversational usage.

## 6. Files

- `collaboration.png` — automation vs. augmentation, all traffic (unadjusted)
- `collaboration_work_only.png` — automation vs. augmentation, work-dominant occupations only, usage-weighted (confound control)
- `use_case.png` — work/personal/coursework mix, by source
- `artifact_type_mix.png` — top 12 output types, by source
- `occupation_category_gap.png` — automation-share gap by SOC major group
- `occupation_api.png` / `occupation_claude.png` — top-10 occupation usage share, by source (context only, not an automation comparison)