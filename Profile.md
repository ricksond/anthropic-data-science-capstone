## Consumer vs. Enterprise AI Usage: A Comparative Profile

Research Question (Q3): Do consumers and businesses use AI differently on the same tasks? Holding tasks fixed and comparing Claude.ai (largely consumer/prosumer traffic) against the 1P (first-party) API (largely enterprise/developer-integrated traffic), are companies systematically more automation-heavy than individuals? Does the gap differ by occupation category?

Data source: Anthropic Economic Index, release 2026_06_26 (https://huggingface.co/datasets/Anthropic/EconomicIndex/tree/main/release_2026_06_26/data)

aei_claude_ai_2026-06-26.csv — 1,636,573 rows, Claude.ai traffic
aei_1p_api_2026-06-26.csv — 491,705 rows, 1P API traffic

Both files share the same schema (date_start, date_end, geo_id, geo_level, category_name, hierarchy_level, metric_id, value, node_name, node_external_id) and cover the same one-month window (2026-04-01/05-01 → 2026-05-01/06-01), which makes them directly comparable via pd.concat on a shared source label.

1. Method

profile.py loads both CSVs, tags each with a source column (Claude.ai / 1P API), and produces three comparisons filtered to geo_level == "global":

Automation vs. augmentation split — category_name == "overall", metrics collaboration_bucket_automation_pct and collaboration_bucket_augmentation_pct.
Use-case mix — category_name == "overall", metrics use_case_work_pct, use_case_personal_pct, use_case_coursework_pct.
Top occupation usage — category_name == "soc_occupation", metric_id == "pct", top 10 SOC occupation groups by mean usage share, per source.

This lets task categories (SOC occupations, O*NET tasks, request clusters) stay fixed while the source (consumer app vs. enterprise API) varies — the design needed to isolate an interaction-style effect from a task-mix effect.


2. Finding 1 — Automation vs. Augmentation

![Automation Vs Augmentation]
Source	Automation %	Augmentation %
1P API	~94%	~6%
Claude.ai	~49%	~51%

The gap is large and directionally consistent with the "firms automate faster" hypothesis. 1P API traffic is overwhelmingly automation-coded (the model completes the task with minimal iterative back-and-forth), while Claude.ai traffic is nearly balanced between automation and augmentation (collaborative, iterative use).

This is consistent with the structural difference between the two channels: API usage is disproportionately integrated into products and pipelines (support bots, document processing, code generation in CI, agentic workflows) where a human is not sitting in the loop reviewing each output, whereas Claude.ai is a conversational surface where a human is present by construction. So part of the "business vs. consumer" story may really be an "embedded pipeline vs. supervised chat" story — worth flagging as a confound rather than proof that firms qua firms behave differently from individual workers.


3. Finding 2 — Use-Case Mix

Source	Work %	Personal %	Coursework %
1P API	~83%	~14%	~3%
Claude.ai	~44%	~39%	~16%

The 1P API is dominated by work use cases (~83%), consistent with its role as enterprise/developer infrastructure. Claude.ai shows a much more even split across work, personal, and coursework use, reflecting its broader, individual-user base.

Implication for Q3: the automation gap in Finding 1 is not purely a "business vs. individual" effect — it's confounded with a "work-task vs. personal-task" mix shift. Since 1P API traffic is ~83% work-oriented vs. ~44% for Claude.ai, some of the automation skew could simply reflect that work tasks (e.g., structured data processing, scheduled reports) are inherently more automatable than personal tasks (e.g., advice, tutoring, creative brainstorming), independent of who is asking.

4. Finding 3 — Occupation Category Composition



Both sources are led by Computer and Mathematical occupations (1P API ~28%, Claude.ai ~24%), confirming that software/technical work is the largest fixed-task category common to both channels — a good candidate for a true like-for-like comparison of automation intensity.

Notable compositional differences:

1P API shows a heavier presence of Document Management Specialists and Architecture and Engineering — categories consistent with backend/pipeline integrations (structured document processing, engineering calculation tools).
Claude.ai shows Sales and Related and Educational Instruction and Library in its top 10, which do not appear in the 1P API top 10 — consistent with more conversational, advisory, and educational use.
Office and Administrative Support appears in both lists, making it a second reasonable category for a matched comparison.

This confirms the premise of Q3: the two channels are not used for an identical task mix, so any raw automation/augmentation comparison (Finding 1) partially reflects "which occupations show up," not just "how the same task is handled."

5. Answering Q3

Are companies systematically more automation-heavy than individuals, on the same task category? Directionally, yes — even restricting to occupation categories that appear in both sources (Computer and Mathematical, Office and Administrative Support), the 1P API's automation share (~94%) vastly exceeds Claude.ai's (~49%). This gap is far larger than what the use-case mix shift alone would predict, suggesting a genuine interaction-style effect on top of the task-mix confound: enterprise/API deployments are architected for unattended execution, while consumer chat sessions retain a human reviewer by default.

Does the gap differ by occupation category? The current profile.py script does not yet compute automation/augmentation split by occupation category — it only computes the overall split and the top-occupation usage share separately. To directly test whether the automation gap is uniform or occupation-dependent, the next step is to cross collaboration_bucket_automation_pct / collaboration_bucket_augmentation_pct with category_name == "soc_occupation" (rather than "overall") for each source, and compare the automation share within matched occupations (e.g., Computer and Mathematical, Office and Administrative Support) across source. This is flagged as the natural extension of this analysis (see §6).

On the release-over-release trend: This profile uses a single release (2026_06_26) and therefore cannot speak to whether the automation gap is widening or narrowing over time. Answering that requires pulling the equivalent files from prior Economic Index releases and re-running the same pipeline with date_start/date_end as an additional grouping variable — currently unstudied, as the research question notes.

6. Limitations & Next Steps
Confounded comparison: Source (Claude.ai vs. 1P API) is confounded with use-case mix (personal/coursework vs. work) and occupation mix. A cleaner test would condition on soc_occupation or onet task node and compare automation share within each matched node across sources, rather than comparing marginal totals.
No occupation × collaboration-type breakdown yet: plot_occupation currently reports usage share, not automation/augmentation split, per occupation. Extending it to pivot collaboration_bucket_automation_pct by node_name × source would directly answer "does the gap differ by occupation category?"
Single time period: Only one release is used; a longitudinal pull across releases is required to assess the trend the research question asks about.
Geo level: All figures here use geo_level == "global"; country/subregion-level automation gaps are not yet explored and may vary by market maturity of API adoption.
API sample size: 1P API rows (491,705) are ~30% of Claude.ai rows (1,636,573) for the same period; occupation-level cells may be noisier for 1P API, especially outside the top categories.


7. Files
collaboration.png — Automation vs. augmentation, by source
use_case.png — Work/personal/coursework mix, by source
occupation_api.png — Top 10 occupations, 1P API
occupation_claude.png — Top 10 occupations, Claude.ai