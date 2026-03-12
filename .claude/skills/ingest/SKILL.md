---
description: "Ingest external research (analyst reports, Substack articles, SEC filings) into the right company folder"
argument: "[TICKER] — Stock ticker the research is about"
---

# Ingest Skill

Organize external research into the standardized company research folder.

## When to Use

You've read an analyst report, Substack article, or other research that you want to keep. This skill files it properly so it's queryable and organized alongside your own analysis.

## Input

Either:
1. Paste content directly in chat
2. Point to a file that needs to be ingested
3. Provide a URL to read and ingest

## Process

### Step 1: Identify the Company

- Normalize ticker to uppercase
- Set target directory: `research/{TICKER}/`
- If the company folder doesn't exist, create it using the template from `research/_TEMPLATE.md`

### Step 2: Identify the Source Type

Classify the research as one of:
- **Analyst Report** → file in `analysts/`
- **Substack/Newsletter** → file in `external/`
- **SEC Filing Notes** → file in `filings/`
- **Earnings Call Notes** → file in `earnings/`
- **News/Commentary** → file in `news/`

Create the subfolder if it doesn't exist.

### Step 3: Extract and Format

Use this standardized format for ALL ingested research:

```markdown
# {Source} — {Title or Headline}

**Date:** YYYY-MM-DD
**Author:** {Author name}
**Source:** {Publication/firm name}
**Type:** {Analyst Rating | Research Article | Earnings Analysis | Commentary}

---

## Rating (if applicable)

| Metric | Value |
|--------|-------|
| Recommendation | {BUY/HOLD/SELL etc.} |
| Target Price | US${XX} |
| Previous TP | US${XX} |

---

## Key Thesis

{2-3 sentence summary of the main argument}

---

## Full Report

{Full content, preserving the author's analysis and data}

---

## Key Metrics

| Metric | Value | YoY Change |
|--------|-------|------------|
| {relevant metrics from the report} |

## Model Changes (if applicable)

| Metric | Old | New | Change |
|--------|-----|-----|--------|

---

*Source: {Full citation}*
```

### Step 4: File Naming

Format: `YYYY-MM-DD-{source-slug}.md`

Examples:
- `2026-03-11-phillips-capital.md`
- `2026-03-11-capitalist-letters.md`
- `2026-03-11-sec-10k-notes.md`

### Step 5: Update Company Overview

If the company has an `overview.md`, append to the updates log section. If not, note the new source for when `/research` is run.

### Step 6: Cross-Reference Check

After filing, briefly note if the new research:
- **Contradicts** your existing thesis (flag it)
- **Updates** key metrics beyond what you have
- **Introduces** new risks or catalysts not in your current analysis

Report these so you can decide if the main research files need updating.

## Multi-Company Research

If the source covers multiple companies:
1. File the full report under the PRIMARY company
2. Create a short reference note in each OTHER company's folder:

```markdown
# Cross-Reference: {Title}

**Primary filing:** `research/{PRIMARY_TICKER}/external/{filename}`
**Date:** YYYY-MM-DD
**Relevant to {THIS_TICKER}:** {1-2 sentence summary of what's relevant}
```

## Quality Standards

- Preserve the original author's data and analysis - don't summarize away detail
- Always include the full report content, not just key points
- Source citation is mandatory on every ingested file
- Numbers must match the source exactly - never estimate or round
