---
description: Pull fresh opportunities from grants.gov, rank against the writer profile, and present a shortlist
allowed-tools: Bash, Read
argument-hint: "[--limit N] [--sync-notion]"
---

You are running the daily grants.gov eligibility scan.

**Steps**

1. Confirm `config/profile.json` exists. If only `config/profile.example.json` is present, tell the user to copy it to `config/profile.json` and edit, then stop.
2. Run the fetch -> enrich -> rank pipeline from the repo root:
   ```bash
   python3 scripts/grants_fetch.py --profile config/profile.json --out data/raw.json
   python3 scripts/enrich.py --raw data/raw.json --profile config/profile.json --out data/enriched.json --top-k 50
   python3 scripts/rank.py --profile config/profile.json --raw data/enriched.json --out data/ranked.json --limit ${LIMIT:-15}
   ```
   The fetch returns hundreds of opportunities. Enrich does a cheap pre-rank on title/agency/ALN, picks the top 50, fetches full descriptions + award amounts for those. The final rank pass re-scores with description matching and award-size filters applied.

   Honor `$ARGUMENTS`:
   - `--limit N` overrides the final result count
   - `--no-enrich` skips enrichment (faster, but no award-size filter or description matching) — use `data/raw.json` directly as input to rank instead

   Tell the user that enrich takes ~10–15 seconds before kicking off, so they aren't surprised by the pause.
3. Read `data/ranked.json`.
4. Present the top results to the user as a compact table: rank, score, title (truncated to 70 chars), agency code, days-to-close, and a one-line "why" assembled from the reasons array. Format as Markdown so it renders well.
5. For the top 3 results, write one extra sentence of "fit reasoning" in the writer's voice — not a generic restatement of the reasons, but a judgment call ("This aligns with your past wins in X because…"). Keep each sentence under 25 words.
6. If `$ARGUMENTS` contains `--sync-notion` AND `profile.json` has `notion.enabled: true` AND a `notion.database_id` is set: use the Notion MCP (`mcp__*notion*-create-pages` or equivalent) to upsert each ranked opportunity into that database. Map fields: Title → name, URL → grants.gov detail URL, Agency → agency, Close Date → closeDate, Score → score, Status → status. If a page with the same opportunity number already exists, update instead of duplicating. If the Notion MCP is unavailable, tell the user clearly rather than silently skipping.
7. End with a one-line summary: total fetched, total ranked, top score.

**Notes**

- Do not invent grants. Only show what `data/ranked.json` actually contains.
- If the fetch script fails (network, API error), surface the stderr to the user. Do not retry silently.
- The grants.gov detail URL is already pre-built into the ranked JSON.
