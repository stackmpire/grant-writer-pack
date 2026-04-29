# Grant Writer Pack

Three slash commands that turn Claude Code into a grant writer's daily workhorse.

- **`/grants-scan`** — daily eligibility scan over grants.gov, filtered to your niche, ranked, with "why this fits" reasoning per opportunity.
- **`/grants-draft`** — point at an RFP URL or PDF, get a Markdown skeleton mapped to the funder's exact rubric (sections, word limits, evaluation criteria, attachments).
- **`/grants-boilerplate`** — retrieve org-capacity / theory-of-change / eval-plan sections from past wins, rewritten in the funder's tone, with a reuse log so you don't repeat language to the same funder.

No API key. No cloud bill. Runs locally on top of Claude Code.

## Install

```bash
git clone <this-repo> grant-writer-pack
cd grant-writer-pack
cp config/profile.example.json config/profile.json
# edit config/profile.json with your keywords, preferred agencies, ALNs
```

That's it. Open the directory in Claude Code and the three slash commands light up.

## Daily use

```
/grants-scan                # top 15 by default
/grants-scan --limit 30
/grants-scan --sync-notion  # also upserts to your Notion DB
```

The scan does two things:

1. Hits the public **grants.gov search2 API** (no auth, no key) for current `posted` and `forecasted` opportunities.
2. Scores each against your `profile.json` — keyword match in title, preferred agency, preferred ALNs, deadline window — and surfaces a ranked shortlist with deterministic "why this fits" reasoning.

The top 3 also get a one-sentence judgment-call from Claude on fit ("This aligns with your past wins in X because…").

## Profile

Edit `config/profile.json`:

```json
{
  "keywords": ["youth mental health", "after school", "rural broadband"],
  "exclude_keywords": ["research", "fellowship"],
  "preferred_agencies": ["HHS", "ED", "USDA"],
  "preferred_alns": ["93.243", "84.287"],
  "min_days_until_deadline": 14,
  "max_days_until_deadline": 180,
  "min_score": 1,
  "rows": 200,
  "notion": {
    "enabled": false,
    "database_id": "..."
  }
}
```

`keywords` runs one search per term and dedupes, so `["youth mental health", "after school"]` produces a union, not an intersection.

## Notion sync (optional)

If you have the Notion MCP connected to Claude Code:

1. Create a Notion database with these properties: **Title** (title), **URL** (URL), **Agency** (text), **Close Date** (date), **Score** (number), **Status** (select).
2. Set `notion.enabled: true` and paste the database ID into `profile.json`.
3. Run `/grants-scan --sync-notion`.

Each opportunity becomes a Notion page; reruns update existing rows by opportunity number rather than duplicating.

## RFP-to-draft

```
/grants-draft https://grants.nih.gov/grants/guide/pa-files/PAR-24-067.html
/grants-draft ./rfps/HRSA-26-001.pdf
```

Output is a Markdown file at `drafts/<slug>.md` with:

- Funder format detected (NIH / NSF / SF-424 / foundation LOI / generic)
- Every required section as an H2 with the funder's exact heading text
- Word/page limits pulled verbatim from the RFP (or `(no stated limit)` if absent)
- Evaluation criteria the reviewer will use
- Attachments checklist
- "Reviewer's first-read test" — three questions a reviewer skims for in 60 seconds

The skeleton is the deliverable; the writer brings the substance.

## Boilerplate vault

```
/grants-boilerplate org capacity for HRSA
/grants-boilerplate theory of change for Robert Wood Johnson --auto
```

Drop your past proposals into `boilerplate/` (`.md` or `.txt`). The command finds matching sections, shows the 3 most relevant, and rewrites the chosen one in the funder's tone. Every reuse is logged to `boilerplate/.reuse-log.jsonl` so you get a warning if you're about to send the same paragraph to the same funder twice in 18 months.

## Files

```
grant-writer-pack/
├── .claude/commands/         # slash commands (grants-scan, grants-draft, grants-boilerplate)
├── config/profile.example.json
├── scripts/
│   ├── grants_fetch.py       # stdlib-only grants.gov fetcher
│   └── rank.py               # filter + score + reason
├── data/                     # raw + ranked JSON output
├── boilerplate/              # drop your past proposals here
└── drafts/                   # generated proposal skeletons
```

## Limits, honestly

- **grants.gov only.** No state portals or private foundation feeds in v1. State portals come next; foundation data (Candid / Instrumentl) requires a paid subscription and is out of scope for v1.
- **Title-only keyword matching.** The search2 API doesn't expose full opportunity descriptions in the list response, so keyword scoring runs on titles. Detail-fetching per opportunity is on the roadmap.
- **No award-amount filter.** The list response doesn't include award size; that field is in the detail endpoint. Add detail-fetch to filter on this.
- **Eligibility codes are coarse.** grants.gov uses 18 broad eligibility categories; if you serve a narrower segment, fine-tune via `keywords` and `exclude_keywords`.

## Pricing (when sold)

- **Solo**: $149/mo — 1 seat, all three commands, unlimited scans.
- **Firm**: $349/mo — 3 seats, shared boilerplate vault, priority email support.
- Annual plans get 2 months free. One won grant pays for ~10 years of subscription.
