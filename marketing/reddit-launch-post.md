# r/grantwriting launch post — DRAFT

> **Read these first before posting:**
>
> 1. r/grantwriting rules at https://www.reddit.com/r/grantwriting/about/rules — confirm self-promotion is allowed for this kind of post (most subs require contributing first / disclosing affiliation / posting to a specific weekly thread).
> 2. Comment helpfully on 5-10 unrelated posts in the sub over a few days **before** this lands. Mods notice account history.
> 3. Account should be at least 30 days old with non-zero karma. Use a real account, not a throwaway.
> 4. Be honest about the paid tier. Pretending it's a "side project" when it's a paid product reads as deceptive and the comments will eat you.
> 5. Reply to every comment in the first 24 hours. The first 3 hours of post engagement determine the entire trajectory.

---

## Title options (pick one)

- **A** — *I built a daily grants.gov scanner for myself, sharing it free if anyone wants it*
- **B** — *Tired of scrolling grants.gov every morning, so I wrote a thing. Free install, would love feedback.*
- **C** — *Built a grants.gov ranker that filters by my niche. Sharing the install + asking what's missing.*

I'd lean **A** — most honest, lowest cringe.

---

## Body

> Solo writer, mostly federal, mostly youth/education. The thing I hate most about Mondays is opening grants.gov and scrolling through 50 things that aren't relevant to find the 2 that are.
>
> I wrote a small thing that does it for me. Pulls from the public grants.gov API every morning, filters by my keywords, preferred agencies, and ALNs, and gives me a ranked shortlist with the deadline math + award sizes already done. Spits the results into a Notion DB I keep open during work hours.
>
> It's a Claude Code plugin (so it runs locally — your past proposals stay on your machine, which mattered to me because some of my clients won't sign data agreements with random SaaS tools). Free to install. Three slash commands:
>
> - `/grants-scan` — the daily ranker
> - `/grants-draft` — turns an RFP URL/PDF into a skeleton with the funder's exact section headings + word limits
> - `/grants-boilerplate` — pulls org-capacity / theory-of-change sections from your past wins, rewrites in the funder's tone, warns before you reuse the same paragraph for the same funder twice
>
> Install: [LINK_TO_REPO]
> One-page overview: [LINK_TO_LANDING_PAGE]
>
> **What I'm asking:** if you try it, tell me what's broken or missing. I'm not Instrumentl — no private foundation data, grants.gov only — but for federal-heavy writers it's already saving me ~3 hours a week.
>
> **Disclosure:** there's a paid tier ($149/mo) for the boilerplate vault and Notion sync. The eligibility scanner is free forever; that's the part that solved my actual problem and I figure others have it too. Mods, happy to delete if this crosses a line.

---

## Why this version

- Personal, not corporate. The "I" voice is the only one r/grantwriting tolerates.
- Names a specific, common pain ("scrolling grants.gov every morning").
- Discloses the paid tier in the body, not the comments — defenders show up when you're upfront.
- Asks for feedback, not signups. The signups come from the install, not the post.
- Calls out what it isn't. r/grantwriting will compare it to Instrumentl in the comments anyway; better to set the comparison yourself.

## What to expect in comments

- "How is this different from Instrumentl?" — Have a clean two-sentence answer ready: lower price, local data, federal-only in v1.
- "What about [state portal X]?" — Roadmap. Ask which portals matter most.
- "I'd pay for the boilerplate vault but not the scanner" — Listen. This is the highest-signal feedback you'll get.
- "Is this AI slop?" — Yes, partly. The reasoning text is templated; the rewrites are model-generated. Don't pretend otherwise.

## Anti-patterns to avoid

- Don't post a screenshot of the landing page — it reads as ad copy.
- Don't open with "Hey grant writers!" — instant downvote signal in this sub.
- Don't crosspost the same body to r/nonprofit on the same day. Stagger by a week and rewrite.
