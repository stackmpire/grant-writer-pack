---
description: Take an RFP URL or PDF and produce a structured response skeleton mapped to the funder's rubric
allowed-tools: Read, Write, WebFetch, Bash
argument-hint: "<url-or-path-to-RFP>"
---

You are scaffolding a grant proposal response.

**Input**: `$ARGUMENTS` — a URL to an RFP/NOFO page, OR a path to a PDF/Markdown file containing the RFP.

**Steps**

1. Fetch / read the RFP content. For URLs, use WebFetch. For local PDFs, use the Read tool (pages: "1-20" if long).
2. Identify the funder format. Pick the closest of: NIH (R01/R03/R21 style), NSF (Project Description), federal SF-424 (Project Narrative), foundation LOI, state agency narrative. If none match, treat as generic.
3. Extract the rubric: every required section, its word/page limit, the evaluation criteria, the attachments list, the deadline, the eligibility requirements, and the award range.
4. Generate a Markdown skeleton at `drafts/<opportunity-slug>.md` with:
   - YAML frontmatter: `funder`, `opportunity_number`, `deadline`, `award_range`, `eligibility`.
   - One H2 per required section, with the funder's exact heading text quoted.
   - Under each H2: the word/page limit, the evaluation criteria the reviewer will use, and 3-5 bullet prompts ("Open with X. Cover Y. Close with Z.") tailored to what that funder values.
   - An "Attachments checklist" section listing every required attachment with a checkbox.
   - A "Reviewer's first-read test" section: 3 questions a reviewer would skim for in the first 60 seconds. The writer's job is to make sure the answers are obvious.
5. Do NOT fill in narrative content. The skeleton is the deliverable — the writer brings the substance.
6. Print the file path and a one-line summary of what was extracted.

**Quality bar**

- Section headings must match the RFP verbatim. Reviewers are checking compliance.
- Word counts must come from the RFP, not guesses. If a limit isn't stated, write `(no stated limit)`.
- If you can't find a deadline, say so explicitly. Don't invent one.
