# HanuAI ML Assessment — Stakeholder Report

## Executive summary
This package supplies runnable workflows for both tasks. The named Task 2 file, `Hanuai task2 assignment.csv`, was not included with the provided documents. No empirical failure rates, sentiment drivers, trends or root causes are claimed; run the analyses with actual data before presenting findings.

## Task 1: public reviews and sentiment
The workflow collects visible public fields (unique key, title, body, date, rating, source URL and public display name), unions sort views, paginates through visible “Show More” controls, and de-duplicates. VADER adds polarity plus a coarse aspect tag. Validate at least 50 unique records, date parsing, rating range and duplicate rate. VADER is English-centric and can misread sarcasm, mixed opinions and domain language; manually review a stratified sample.

### Responsible collection and blockers
- Check current Best Buy Canada terms, robots guidance, and applicable privacy rules. Collect only necessary public fields and use conservative pauses.
- The script does not bypass CAPTCHAs, login walls, bot checks or access controls. On a challenge or denial, stop and request authorized access or use an approved interface/export.
- Bound retries with exponential backoff for transient failures, cap attempts and honor server retry instructions. Do not repeatedly request blocked pages.
- Do not use CAPTCHA solving or proxy rotation to evade controls. Truthful browser headers do not confer permission; avoid stealth plugins and identity rotation. If an authorized agreement permits proxies, keep use within its written scope and rate limits.

### Business findings to populate after execution
Report positive/negative/neutral shares, rating distribution, sentiment by rating, recurring aspect tags and anonymized illustrative excerpts. Use evidence from the actual corpus to prioritize product design, reliability, setup guidance or support improvements; sentiment tags do not establish causality.

## Task 2: EDA and text mining
The workflow reports shape, types, missingness and duplicates; removes exact duplicate rows; detects or accepts a narrative column; applies transparent phrase dictionaries for electrical, component, software/control, assembly and performance/quality issues; and fits exploratory TF-IDF/K-Means topic groups where there are sufficient records. It exports enriched rows, statistics, missingness, category counts, cluster keywords and a chart.

### Stakeholder actions
1. Prioritize the most frequent validated categories and compare by product, period, region or component when available.
2. Compare rates with sales/service exposure denominators; complaint counts alone may reflect volume and reporting behavior.
3. Investigate repeat patterns with engineering failure analysis and supplier/lot traceability. Treat text-derived root causes as hypotheses.
4. Apply confirmed findings to quality checks, supplier corrective action, installation documentation, firmware monitoring or support workflows.
5. Track post-change complaint rates and customer outcomes, accounting for seasonality and product mix.

## Learnings and next steps
Phrase tags and clusters are interpretable starting points, not validated production classifiers. Have subject experts label a sample, build a benchmark, measure precision/recall, expand terms to the source language, assess missingness/reporting bias, and compare more advanced topic models only when they improve reviewability. Document coverage, exclusions and confidence limits in final stakeholder materials.

## Limitations
No product URL/review corpus or Task 2 CSV accompanied the files. Site markup and access rules may change; selectors require validation. This is an executable framework and reporting template, not fabricated data analysis. The source CSV is required for empirical Task 2 conclusions.
