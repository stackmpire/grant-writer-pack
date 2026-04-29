# 14-day ship checklist

> Goal: first paying customer by day 14. First $1,500 MRR by day 60.
> If you're not on track by day 7, the diagnosis is usually outreach volume, not product.

## Day 1 — environment

- [ ] Pick a domain. `grantwriterpack.com` or similar. ~$12/yr at Porkbun or Cloudflare. Or skip and use a free `*.carrd.co` subdomain for v1.
- [ ] Set up a fresh email at the domain (or a Gmail alias you don't mind exposing). Don't use your personal email.
- [ ] Push the repo to GitHub. **Make it public** — install instructions read better when people can browse the code.
- [ ] Enable GitHub Pages on the repo, point at `marketing/landing.html` (rename to `marketing/index.html` and set Pages source to `/marketing` on the main branch).
- [ ] Replace `YOUR_EMAIL@example.com` and `[LINK_TO_REPO]` / `[LINK_TO_LANDING_PAGE]` placeholders in landing.html, reddit-launch-post.md, and cold-emails.md.

## Day 2 — install path

- [ ] Walk through the README on a fresh machine (or a blank user account). Time how long install takes. If it's >10 minutes, simplify.
- [ ] Record a 4-minute Loom: profile edit → /grants-scan → showing the ranked output → /grants-draft on a real RFP. Embed in landing.html.
- [ ] Add an FAQ section to landing.html: "Do my proposals leave my machine?" (no), "What if grants.gov goes down?" (you see an error, no silent failures), "Can I cancel anytime?" (yes), "What about state portals?" (roadmap).

## Day 3 — payment plumbing (defer until first interest signal)

- [ ] Stripe payment links: one for $79/mo (early-bird), one for $149/mo, one for $349/mo firm. No subscription billing infra needed yet.
- [ ] Manual provisioning script: when someone pays, send them an email with their license key and the install link. Stay manual until 20+ customers — every one is a feedback conversation.
- [ ] **Don't add a Stripe checkout button yet.** Lead with email-to-buy. Forces conversation, filters tire-kickers, gives you the data on what objection patterns exist.

## Day 4-5 — community presence (before posting anything promotional)

- [ ] Make 5-10 helpful comments on r/grantwriting unrelated to your product. Mod good will is bought, not asked for.
- [ ] Same for any grant-writer Slack/Discord you can join. **Lurk a week** before mentioning the tool.
- [ ] Build the GPA prospect list: 50 names, with one personalization hook each. Spreadsheet format: name, firm, niche, hook, status.

## Day 6-7 — first 10 outreach emails

- [ ] Send 10 cold emails (Variant A by default). Track replies in your spreadsheet.
- [ ] Reply to every response within 4 hours during business hours.
- [ ] If nobody replies by day 8: rewrite the subject line, not the body. Subject lines do most of the work.

## Day 8-9 — first install conversations

- [ ] For everyone who installs: send a "did it work?" check-in at +24h. Half won't respond — that's signal.
- [ ] For everyone who replies: book a 15-min call. Use Cal.com (free). Always end the call by asking "what would have to be true for you to pay $79/mo for this?"
- [ ] Log objections verbatim. Look for the same one twice — that's your day-10 priority fix.

## Day 10 — fix the #1 objection

- [ ] Whatever the most-repeated objection is, fix or counter it. Examples that have come up before with similar tools:
  - "I need state portals" → ship one state (start with the one most common in your prospect list)
  - "I don't trust the ranker" → expose the score formula in the README, or let users adjust weights
  - "Notion sync is the only useful piece" → make it the headline feature
- [ ] Push the fix. Email the people who raised it. **This is your highest-converting email of the whole run.**

## Day 11 — Reddit post

- [ ] Post to r/grantwriting using the draft in `marketing/reddit-launch-post.md` (Variant A title).
- [ ] Reply to every comment within 30 minutes for the first 3 hours.
- [ ] When the post drops off the front page (typically day +1), DM everyone who upvoted with a thank-you and a link to the install if they haven't already.

## Day 12 — second outreach batch

- [ ] Send 20 more cold emails. Mix in Variant B for prospects with grant-writer backgrounds in their bio.
- [ ] Reach out to 3 grant-writer podcasts / newsletters. Pitch a guest post or interview. The Grant Doctor, GrantStation Insider, etc.
- [ ] Post a single tweet/Bluesky thread linking the landing page. Include the Loom. Tag relevant accounts but don't spam.

## Day 13 — first paying customer push

- [ ] Email everyone who installed but hasn't paid: "Early-bird $79/mo locks in this week. Worth a 15-min call to walk through your profile?"
- [ ] Anyone who scheduled a call this week: send them the Stripe link 30 mins before the call ends.
- [ ] Anyone who said "I'd pay if X": email them the moment X ships.

## Day 14 — review

- [ ] Count: installs, calls booked, calls done, paying customers, MRR.
- [ ] Realistic numbers: 30+ installs, 8+ calls, 3+ paying. Below that, it's outreach volume, not product. Above that, ship the next pack faster.
- [ ] **Do not start the second pack (bookkeeper) until Grant Writer Pack hits $3K MRR.** One pack at $3K beats two packs at $500. Focus is the asset.

---

## Kill criteria — when to stop

- **50 cold emails sent + 0 paying customers + no consistent objection theme** — the segment is wrong or the price is wrong. Drop to $49/mo and re-run, or pivot to Bookkeeper Pack.
- **10+ installs but nobody finishes the install** — the install path is too hard. Stop selling, fix the path, restart.
- **First paying customer churns at month 2** — interview them. If they say "didn't end up using it," the daily-habit hook isn't strong enough. Build a daily email digest before scaling outreach further.

## Don't do

- Don't add features customers haven't asked for.
- Don't build a second product before the first hits $3K MRR.
- Don't post to LinkedIn. Wrong audience for this tool, will burn time you could spend on GPA outreach.
- Don't run paid ads in v1. Distribution math doesn't work below $1K MRR.
