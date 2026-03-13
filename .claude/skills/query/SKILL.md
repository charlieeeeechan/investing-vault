---
description: "Query across all stored research to answer investing questions using your curated data"
argument: "[QUESTION] — Any investing question (e.g., 'What is AAPL cloud revenue growth?' or 'Compare MSFT vs GOOGL margins')"
---

# Query Skill

Answer investing questions by searching your curated research files FIRST, before using external sources.

## Why This Exists

Your research folder contains quality-verified data from:
- Your own SEC EDGAR analysis (via `/research`)
- Analyst reports you've read and vetted (via `/ingest`)
- Earnings analysis (via `/earnings`)
- Bear case deep dives (via `/stress-test`)
- Company comparisons (via `/compare`)

This data is MORE trusted than random web results. Always use it first.

## Process

### Step 1: Understand the Question

Parse what's being asked:
- **Single company:** "What's AAPL's iPhone revenue growth?" → search `research/AAPL/`
- **Cross-company:** "Compare cloud revenue: AMZN vs MSFT vs GOOGL" → search all three
- **Thematic:** "Which companies have the highest margins?" → scan across all research
- **Source-specific:** "What did Phillips Capital say about AAPL?" → search analyst reports

### Step 2: Search Local Research First

Search in this order:

1. **`research/{TICKER}/`** — primary research files
   - `overview.md` (thesis, bull/bear case, catalysts)
   - `financials/` (income, balance, cashflow, metrics)
   - `valuation.md` (DCF, multiples, scenarios)
   - `analysts/` (external analyst reports)
   - `external/` (Substack, newsletter research)
   - `earnings/` (quarterly analysis)

2. **`research/comparisons/`** — existing company comparisons

3. **`macro/`** — macro themes and weekly notes

4. **`portfolio/`** — portfolio context and position sizing

### Step 3: Compile Answer

When answering:

- **Cite the source file:** `(Source: research/AAPL/analysts/2026-02-02-phillips-capital.md)`
- **Cite the original source within that file:** `(Phillips Capital, Helena Wang, 2026-02-02)`
- **Flag data freshness:** If the data is older than 3 months, note it
- **Flag gaps:** If the question can't be fully answered from stored data, say what's missing

### Step 4: Cross-Reference (for multi-company queries)

When comparing across companies:
- Build a comparison table with data from each company's files
- Note which data points come from which sources
- Flag if data periods don't match (e.g., AAPL FY ends Sept, MSFT FY ends June)
- Highlight where analysts disagree with each other or with your own analysis

### Step 5: Extend If Needed

If stored research doesn't fully answer the question:
1. First, report what you DID find and from which sources
2. Ask if the user wants external research
3. If yes, clearly mark external data as `(Source: Web research, not yet verified)`
4. Suggest running `/ingest` on any new quality sources found

## Output Format

```markdown
## Answer

{Direct answer to the question}

## Data

{Tables, numbers, comparisons - whatever the question requires}

## Sources Used

| Source | File | Date | Type |
|--------|------|------|------|
| {Original source} | {File path} | {Date} | {Analyst/SEC/External} |

## Data Gaps

{What couldn't be answered from stored research, if anything}
```

## Key Rules

- NEVER make up numbers. If the data isn't in the files, say so.
- Local curated data > web research. Always.
- Preserve source attribution chain: your file → original source
- If multiple sources give different numbers for the same metric, show both and note the discrepancy
