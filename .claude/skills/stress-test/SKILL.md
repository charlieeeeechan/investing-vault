---
description: "Stress-test your investment thesis — contrarian analysis + tripwires"
argument: "[TICKER] — Stock ticker symbol"
---

# Stress Test Skill

Stress-test the investment thesis for the given ticker and append it to the existing research.

## Prerequisites

1. Normalize the ticker to uppercase.
2. Check if `research/{TICKER}/overview.md` exists.
   - If it does NOT exist, tell the user: "No existing research found for {TICKER}. Run `/research {TICKER}` first to build the base thesis before generating a bear case."
   - Stop execution.
3. Read `research/{TICKER}/overview.md` — understand the current thesis, bull case, and existing bear case.
4. Read `research/{TICKER}/financials/income-statement.md`, `balance-sheet.md`, `cash-flow.md` for financial context.
5. Read `research/{TICKER}/valuation.md` if it exists, for valuation context.
6. Read any existing earnings files in `research/{TICKER}/earnings/` for recent trend data.

## Step 1: Summarize Current Thesis

Extract from `overview.md`:
- The investment thesis (one-paragraph summary)
- The bull case points
- The existing bear case points (if any)
- Key metrics being watched

This becomes the "Thesis Summary" section of the bear case.

## Step 2: Build the Bear Case

Think deeply and critically. The goal is NOT to be blindly negative — it is to stress-test the thesis with the strongest possible counterarguments. Consider:

**Structural / Business Risks:**
- Is the moat actually narrower than assumed?
- Are switching costs real or theoretical?
- Could a technology shift make the product irrelevant?
- Is the TAM overestimated?

**Financial Risks:**
- Revenue quality (recurring vs project-based, customer concentration)
- Margin sustainability (input costs, pricing power, competition)
- Balance sheet risks (debt maturity, covenant risk, pension obligations)
- Cash flow quality (working capital manipulation, capex deferral)
- Accounting concerns (revenue recognition, aggressive assumptions)

**Competitive Risks:**
- Who is the most dangerous competitor and why?
- Could a well-funded new entrant disrupt the market?
- Is the company winning or losing share in key segments?

**Macro / External Risks:**
- Regulatory risk (antitrust, data privacy, sector-specific)
- Geopolitical exposure
- Interest rate / currency sensitivity
- Cyclicality that the bull case ignores

## Step 3: Write the Bear Case Section

Append a `## Bear Case Deep Dive` section to `overview.md` with this structure:

```markdown
## Bear Case Deep Dive

*Generated: {YYYY-MM-DD}*

### Thesis Summary
[1-2 paragraph summary of the current bull thesis from overview.md]

### The Bear Case

**1. [First Bear Argument — clear, specific title]**
[2-3 sentences explaining the argument with data if available]

**2. [Second Bear Argument]**
[...]

**3. [Third Bear Argument]**
[...]

**4. [Fourth Bear Argument]**
[...]

**5. [Fifth Bear Argument]**
[...]

(Include 5-7 arguments total. Each should be specific and substantive, not generic.)

### Financial Red Flags
- [Specific financial concern with data point]
- [Another concern]
- [Another concern]

### Competitive Threats
| Threat | From Whom | Severity | Timeline |
|--------|-----------|----------|----------|
| [Specific threat] | [Competitor] | High/Med/Low | Near/Mid/Long |
| [...] | [...] | [...] | [...] |

### Valuation Concerns
- What the current price implies about growth/margins
- Where consensus estimates might be too optimistic
- Historical valuation range and where it sits now
- What a bear-case DCF would look like (reference tools/dcf_calculator.py)

### What Would Prove The Bears Right
A clear list of observable, falsifiable signals:
1. [Specific metric dropping below X]
2. [Specific competitive event]
3. [Specific financial threshold]
4. [Specific management action]

These are tripwires — if they trigger, the thesis needs serious re-examination.

### Counterarguments (Why Bulls Might Still Win)
For intellectual honesty, briefly acknowledge the strongest bull rebuttals:
1. [Rebuttal to bear point 1]
2. [Rebuttal to bear point 2]
3. [Rebuttal to bear point 3]

### Bear Case Fair Value
- Estimated downside price target with assumptions
- Margin of safety assessment: is the current price pricing in the bull case, base case, or already discounting risks?
```

## Step 4: Summary

Print a summary:
```
Bear case analysis complete for {TICKER}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Arguments generated: {N}
Red flags identified: {N}
Competitive threats mapped: {N}
Tripwires defined: {N}

Appended to: research/{TICKER}/overview.md (## Bear Case Deep Dive)

Key takeaway: [One sentence — is this a "thesis risk" or "thesis killer"?]
```
