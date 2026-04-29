---
description: Retrieve and rewrite reusable proposal sections (org capacity, mission, eval plan) from past wins
allowed-tools: Read, Write, Glob, Grep, Bash
argument-hint: "<section-type> for <funder-name>"
---

You are pulling from the writer's boilerplate vault.

**Input**: `$ARGUMENTS` — describes what's needed, e.g., "org capacity for HRSA" or "theory of change for Robert Wood Johnson".

**Steps**

1. Look in `boilerplate/` for past proposal files (`.md`, `.txt`). If the directory is empty, tell the user to drop past proposals there and stop.
2. Use Grep to find sections matching the requested type. Common headers: "Organizational Capacity", "Statement of Need", "Theory of Change", "Evaluation Plan", "Mission", "Project Approach".
3. Surface the 3 most relevant past versions. Show: source filename, length, and first 200 chars.
4. Ask the user to pick one (or auto-pick the most recent if `--auto` is in $ARGUMENTS).
5. Rewrite the chosen section in the funder's tone:
   - Federal agencies: formal, jargon-aware, third person, bureaucratic-but-clear.
   - Foundations: warmer, story-led, uses beneficiary language.
   - State agencies: reference state-specific frameworks if known.
6. Write the rewrite to `drafts/<funder-slug>-<section-slug>.md` and log the source-to-target mapping in `boilerplate/.reuse-log.jsonl` (one line per reuse: `{"date": "...", "source": "...", "target": "...", "funder": "..."}`).
7. Warn if the same source paragraph has been used for the same funder in the last 18 months — funders notice copy-paste.

**Quality bar**

- Preserve specific numbers, names, and outcomes from the source. Don't paraphrase metrics into vagueness.
- Match the funder's stated values. If their RFP emphasizes "equity" or "evidence-based", the rewrite should land on those words.
