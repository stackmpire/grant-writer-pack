# Grant Writer Pack — CLAUDE.md

A Claude Code plugin that gives solo grant writers a daily grants.gov scanner, RFP-to-skeleton drafter, and a local boilerplate vault. This is a commercial product at $149/mo (Solo) / $349/mo (Firm).

## Project layout

```
scripts/
  grants_fetch.py   — hits grants.gov search2 API, writes data/raw.json
  enrich.py         — pre-ranks, fetches full detail for top K, writes data/enriched.json
  rank.py           — filters + scores + reasons, writes data/ranked.json
  license.py        — SQLite license key CRUD
  provision.py      — generate key + send welcome email via SMTP
  webhook.py        — Stripe webhook server (stdlib only, no deps)
  daily-scan.sh     — shell wrapper for the LaunchAgent cron

.claude/commands/
  grants-scan.md        — daily eligibility scanner slash command
  grants-draft.md       — RFP-to-skeleton slash command
  grants-boilerplate.md — past-wins retrieval slash command

config/
  profile.example.json  — template; user copies to profile.json

boilerplate/            — user's past proposals (.md or .txt)
drafts/                 — generated proposal skeletons
data/                   — raw.json, enriched.json, ranked.json, licenses.db (gitignored)
marketing/              — landing.html, checkout.html, email templates, outreach drafts
```

## Pipeline

```
grants_fetch.py → data/raw.json
enrich.py       → data/enriched.json  (detail-fetch top 50: awardCeiling, synopsisDesc)
rank.py         → data/ranked.json    (score: keyword title match +3, desc match +1,
                                       preferred agency +2, preferred ALN +4,
                                       award out-of-range −1 to −4, excluded keyword −5)
```

## Slash commands

`/grants-scan [--limit N] [--no-enrich] [--sync-notion]`
`/grants-draft <url-or-path-to-pdf>`
`/grants-boilerplate <section-type> for <funder> [--auto]`

## Revenue setup checklist

- [ ] Set REPO_URL and LANDING_URL in scripts/provision.py env vars
- [ ] Set SMTP_HOST / SMTP_PORT / SMTP_USER / SMTP_PASS for license delivery emails
- [ ] Create Stripe account + 3 products (early_bird $79, solo $149, firm $349)
- [ ] Set STRIPE_SECRET_KEY and STRIPE_WEBHOOK_SECRET
- [ ] Replace placeholders in marketing/checkout.html (publishable key, price IDs)
- [ ] Replace YOUR_EMAIL@example.com in marketing/landing.html
- [ ] Replace YOUR_USERNAME in install.sh

## When someone buys (manual flow until webhook is deployed)

```bash
python3 scripts/provision.py --email CUSTOMER_EMAIL --plan solo --stripe-id STRIPE_SESSION_ID
```

## When someone cancels

```bash
python3 scripts/license.py revoke --key XXXX-XXXX-XXXX-XXXX
```

## Pricing

| Plan       | Price   | Seats | Notes                        |
|------------|---------|-------|------------------------------|
| early_bird | $79/mo  | 1     | First 25 customers, locked   |
| solo       | $149/mo | 1     | Standard                     |
| firm       | $349/mo | 3     | Shared boilerplate vault     |

## Roadmap (ship after first $3K MRR)

1. State portal connectors (start with Grants.Illinois, Grants.California)
2. Award-size filter UI in profile (currently in JSON)
3. /grants-status — checks which submitted apps are still pending
4. Candid / Instrumentl integration for private foundations (requires their API key)
