# Investing Vault

An AI-powered investing research vault. Use with [Claude Code](https://docs.anthropic.com/en/docs/claude-code) and optionally [Obsidian](https://obsidian.md) for a complete equity research workflow.

---

## Setup

### Tier 1: Ready in 30 seconds

1. Install [Claude Code](https://docs.anthropic.com/en/docs/claude-code) if you haven't already
2. Open a terminal in this folder
3. Run `claude`

That's it. The `CLAUDE.md` file configures Claude as your investing analyst automatically.

**Try it:** Ask Claude to "summarize the AAPL research" — it'll read the pre-filled example and give you a rundown.

### Tier 2: Explore the vault (10 minutes)

1. Install [Obsidian](https://obsidian.md) (free)
2. Open this folder as a vault: `File > Open folder as vault`
3. Browse the structure:
   - `research/AAPL/` — Pre-filled example showing what a completed research note looks like
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
| `/earnings [TICKER]` | Analyze latest quarterly earnings |
| `/bear-case [TICKER]` | Generate a structured contrarian analysis |
| `/compare [T1] [T2]` | Side-by-side comparison of two companies |
| `/portfolio-review` | Review your portfolio for thesis drift and concentration risk |

**Try it:** Run `claude` and type `/research MSFT` to generate a full research package.

### SEC EDGAR Integration

The skills fetch real financial data from SEC EDGAR (free, no API key needed). You just need Python with `requests`:

```bash
pip install requests
```

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
