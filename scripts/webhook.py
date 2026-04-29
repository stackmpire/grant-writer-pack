#!/usr/bin/env python3
"""Minimal Stripe webhook handler.

Listens for checkout.session.completed → provisions license + sends welcome email.
Listens for customer.subscription.deleted → revokes license.

Run locally for testing:
    stripe listen --forward-to localhost:4242/webhook   (needs Stripe CLI)
    python3 webhook.py

Deploy to any server with:
    python3 webhook.py --host 0.0.0.0 --port 4242

Env vars (required in production):
    STRIPE_SECRET_KEY         sk_live_...
    STRIPE_WEBHOOK_SECRET     whsec_...
    SMTP_HOST / SMTP_PORT / SMTP_USER / SMTP_PASS
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import sys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

from provision import welcome_email, send
from license import generate, revoke, list_all

STRIPE_SECRET = os.environ.get("STRIPE_SECRET_KEY", "")
WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")

PLAN_MAP = {
    "Grant Writer Pack — Early Bird": "early_bird",
    "Grant Writer Pack — Solo": "solo",
    "Grant Writer Pack — Firm": "firm",
}


def verify_signature(body: bytes, sig_header: str) -> bool:
    if not WEBHOOK_SECRET:
        return True
    try:
        parts = {k: v for part in sig_header.split(",") for k, v in [part.split("=", 1)]}
        timestamp = int(parts["t"])
        if abs(time.time() - timestamp) > 300:
            return False
        expected = hmac.new(
            WEBHOOK_SECRET.encode(), f"{timestamp}.".encode() + body, hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, parts.get("v1", ""))
    except Exception:
        return False


def handle_event(event: dict) -> str:
    t = event.get("type")
    data = event.get("data", {}).get("object", {})

    if t == "checkout.session.completed":
        email = (data.get("customer_details") or {}).get("email") or data.get("customer_email")
        stripe_id = data.get("id")
        line_items_url = data.get("url")

        # Determine plan from metadata if set, else default solo
        plan = (data.get("metadata") or {}).get("plan", "solo")
        plan = PLAN_MAP.get(plan, plan)

        key = generate(email, plan, stripe_id)
        body = welcome_email(email, key, plan)
        send(email, f"Your Grant Writer Pack license key — {key}", body)
        print(f"[provision] {email} → {plan} → {key}")
        return "provisioned"

    if t == "customer.subscription.deleted":
        cid = data.get("customer")
        rows = list_all()
        revoked_keys = []
        for row in rows:
            if row.get("stripe_id") and cid in str(row.get("stripe_id", "")):
                revoke(row["key"])
                revoked_keys.append(row["key"])
        print(f"[revoke] customer={cid} keys={revoked_keys}")
        return f"revoked {len(revoked_keys)} key(s)"

    return "ignored"


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/webhook":
            self.send_response(404); self.end_headers(); return
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        sig = self.headers.get("Stripe-Signature", "")
        if not verify_signature(body, sig):
            self.send_response(400); self.end_headers()
            self.wfile.write(b"Bad signature"); return
        try:
            event = json.loads(body)
            result = handle_event(event)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": result}).encode())
        except Exception as e:
            print(f"[error] {e}", file=sys.stderr)
            self.send_response(500); self.end_headers()

    def log_message(self, fmt, *args):
        print(fmt % args)


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=4242)
    args = ap.parse_args()
    print(f"Webhook server on http://{args.host}:{args.port}/webhook")
    HTTPServer((args.host, args.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
