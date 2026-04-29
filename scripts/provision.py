#!/usr/bin/env python3
"""Provision a new customer: generate license key + send welcome email.

Requires env vars:
    SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS  (e.g. Gmail app password)
    SENDER_NAME  (defaults to "Grant Writer Pack")
    REPO_URL     (your GitHub repo URL)
    LANDING_URL  (your landing page URL)

Usage:
    python3 provision.py --email customer@example.com --plan solo
    python3 provision.py --email firm@example.com --plan firm --stripe-id cs_live_xxx
"""

from __future__ import annotations

import argparse
import os
import smtplib
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from license import generate

REPO_URL = os.environ.get("REPO_URL", "https://github.com/stackmpire/grant-writer-pack")
LANDING_URL = os.environ.get("LANDING_URL", "https://grantwriterpack.com")
SENDER_NAME = os.environ.get("SENDER_NAME", "Grant Writer Pack")
SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")

PRICES = {"solo": "$149/mo", "firm": "$349/mo", "early_bird": "$79/mo (locked for life)"}
SEATS = {"solo": "1 seat", "firm": "3 seats", "early_bird": "1 seat"}


def welcome_email(to_email: str, key: str, plan: str) -> str:
    seats = SEATS.get(plan, "1 seat")
    price = PRICES.get(plan, "")
    return f"""\
Hi,

Thanks for subscribing to Grant Writer Pack ({plan.replace("_", " ").title()} — {seats}, {price}).

Your license key is:

    {key}

You'll need this to unlock the full toolkit after install.

---

INSTALL IN 3 STEPS

1. Clone the repo:
   git clone {REPO_URL} grant-writer-pack
   cd grant-writer-pack

2. Copy and configure your profile:
   cp config/profile.example.json config/profile.json
   # Edit config/profile.json with your keywords, agencies, and ALNs
   # (Open it in any text editor — comments explain each field)

3. Open this folder in Claude Code:
   claude .
   # Then type /grants-scan — your first shortlist runs in ~30 seconds.

---

WHAT'S IN THE BOX

/grants-scan       Daily grants.gov scan, filtered + ranked to your niche.
                   Add --sync-notion to pipe results into a Notion database.
                   Add --no-enrich for a faster scan without award-size filters.

/grants-draft <url-or-pdf>
                   Turns an RFP into a Markdown skeleton: every required section,
                   the funder's exact heading text, word limits, and rubric.

/grants-boilerplate <section> for <funder>
                   Pulls matching sections from your past proposals in boilerplate/,
                   rewrites in the funder's tone, logs every reuse.

---

FIRST 10 MINUTES

• Edit config/profile.json — the most important fields are "keywords" and "preferred_agencies".
  Use the agency codes from grants.gov (HHS, ED, USDA, DOJ, etc.).
• Drop 2-3 past proposals into the boilerplate/ folder as .txt or .md files.
  /grants-boilerplate won't be useful until there's something to pull from.
• Run /grants-scan. If the results don't look right, tune the profile and run again.
  It re-fetches live from grants.gov every time.

---

Questions? Reply to this email. I read every one.

{SENDER_NAME}
{LANDING_URL}

---
To cancel: reply "cancel" and I'll stop the subscription. No forms.
"""


def send(to_email: str, subject: str, body: str) -> None:
    if not SMTP_USER:
        print(f"[dry-run] Would send to {to_email}")
        print(f"Subject: {subject}")
        print(body)
        return
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{SENDER_NAME} <{SMTP_USER}>"
    msg["To"] = to_email
    msg.attach(MIMEText(body, "plain"))
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
        s.starttls()
        s.login(SMTP_USER, SMTP_PASS)
        s.sendmail(SMTP_USER, to_email, msg.as_string())
    print(f"Email sent to {to_email}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--email", required=True)
    ap.add_argument("--plan", choices=["solo", "firm", "early_bird"], default="solo")
    ap.add_argument("--stripe-id")
    ap.add_argument("--dry-run", action="store_true", help="Print email without sending")
    args = ap.parse_args()

    if args.dry_run:
        global SMTP_USER
        SMTP_USER = ""

    key = generate(args.email, args.plan, getattr(args, "stripe_id", None))
    print(f"License key: {key}")

    body = welcome_email(args.email, key, args.plan)
    send(args.email, f"Your Grant Writer Pack license key — {key}", body)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
