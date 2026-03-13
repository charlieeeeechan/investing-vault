# Investing Vault

An AI-powered investing research vault. Use with [Claude Code](https://docs.anthropic.com/en/docs/claude-code) and optionally [Obsidian](https://obsidian.md) for a complete equity research workflow.

---

## Setup

### Tier 1: Ready in 30 seconds

1. Install [Claude Code](https://docs.anthropic.com/en/docs/claude-code) if you haven't already
2. Open a terminal in this folder
3. Run `claude`

That's it. The `CLAUDE.md` file configures Claude as your investing analyst automatically.

**Try it:** Type `/research TSLA` and watch Claude pull 5 years of SEC filings, build the research folder, and run a full DCF — all from one command.

### Tier 2: Explore the vault (10 minutes)

1. Install [Obsidian](https://obsidian.md) (free)
2. Open this folder as a vault: `File > Open folder as vault`
3. Browse the structure:
   - `research/` — Your research folder. Run `/research TSLA` to generate your first dossier.
   - `research/_TEMPLATE.md` — Start here when researching a new company
   - `portfolio/` — Track your holdings and watchlist
   - `decisions/` — Decision journal for buy/sell/hold reasoning
   - `macro/` — Market themes and weekly notes

**Try it:** Open `research/_TEMPLATE.md`, duplicate it, and start filling it in for a company you're interested in.

### Tier 3: Custom skills (20 minutes)

This vault includes Claude Code skills (slash commands) that automate common research tasks:

| Command | What it does |
|---------|-------------|
| `/research [TICKER]` | Full company research — business, moat, financials, valuation |
| `/bear-case [TICKER]` | Generate a structured contrarian analysis with tripwires |
| `/earnings [TICKER]` | Analyze latest quarterly earnings + update financials |
| `/thesis-check [TICKER]` | Validate your thesis against latest SEC data |
| `/portfolio-review` | Review all holdings for thesis drift and concentration risk |
| `/compare [T1] [T2]` | Side-by-side comparison of two companies |
| `/query` | Query across all stored research to answer investing questions |
| `/ingest` | Ingest external research (analyst reports, articles) into company folders |

**Try it:** Run `claude` and type `/research MSFT` to generate a full research package.

### Recommended Workflow

The skills are designed to work together in a specific order. Understanding this flow is key to getting the most out of the vault.

#### First time researching a company

```
/research AAPL          Pull 5 years of SEC data, generate research folder
       ↓
  ✏️ Edit overview.md     Make the thesis YOURS — adjust bull/bear case,
       ↓                 set key metrics to watch, add personal thresholds
/bear-case AAPL         Generate contrarian analysis + tripwires
                        (based on YOUR thesis, not the AI's)
```

> **Why the edit step matters:** `/research` generates an AI-written thesis as a starting point. If you skip editing it, every subsequent command validates assumptions you never agreed with. Take 5 minutes to make it yours.

#### After each earnings release

```
/earnings AAPL          Fetch latest quarterly data, update financials
       ↓
/thesis-check AAPL      Check: is your thesis still holding?
                        (On Track → Monitor → Drifting → Broken)
```

`/earnings` only handles data — it pulls the quarter, updates your tables, and stops. `/thesis-check` does the thinking — it reads your thesis, checks each metric and tripwire against fresh SEC data, and gives you a verdict.

#### Quarterly portfolio review

```
/portfolio-review       Check ALL holdings at once — drift, concentration,
       ↓                correlated bets, conviction ranking
/thesis-check [TICK]    Deep-dive any holding flagged as Drifting or Broken
```

#### Anytime

```
/compare AAPL MSFT      Side-by-side comparison of two companies
/query "question"       Ask anything across your stored research
/ingest                 File an analyst report or article into the right folder
```

### Python Dependencies

The skills fetch financial data from SEC EDGAR and live market prices from Yahoo Finance. Install the dependencies:

```bash
pip install -r requirements.txt
```

Or individually:

```bash
pip install requests yfinance
```

- **`requests`** — SEC EDGAR API calls (fundamentals, filings)
- **`yfinance`** — Live stock price, market cap, and EV (sourced from Yahoo Finance, clearly labelled in output)

---

## Structure

```
investing-vault/
├── CLAUDE.md                    # AI analyst configuration
├── research/
│   ├── _SCHEMA.md               # Financial data standards
│   ├── _TEMPLATE.md             # New company template
│   └── AAPL/                    # Example (pre-filled)
├── portfolio/
│   ├── positions.md             # Current holdings
│   ├── watchlist.md             # Stocks you're tracking
│   └── quarterly-reviews/       # Periodic portfolio reviews
├── decisions/                   # Decision journal
├── macro/
│   ├── themes/                  # Macro investment themes
│   └── weekly/                  # Weekly market notes
└── tools/
    └── dcf_calculator.py        # DCF model with sensitivity analysis
```

---

## Troubleshooting

**Claude doesn't seem to know about the vault structure**
Make sure you're running `claude` from inside this folder. The `CLAUDE.md` file only loads when Claude Code starts in the same directory.

**Skills don't appear in autocomplete**
Skills require Claude Code v1.0+. Update with `npm install -g @anthropic-ai/claude-code`. After updating, restart Claude Code.

**SEC EDGAR requests fail**
SEC requires a `User-Agent` header with your email. The skills handle this, but if you hit rate limits, wait 10 seconds and retry. SEC allows 10 requests/second.

---

Built for the [Carepital](https://youtube.com/@carepital) community.
