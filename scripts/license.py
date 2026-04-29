#!/usr/bin/env python3
"""License key management — generate, verify, and revoke.

Stores keys in SQLite at data/licenses.db.
No external deps. Generates XXXX-XXXX-XXXX-XXXX style keys.

Usage:
    python3 license.py generate --email user@example.com --plan solo
    python3 license.py verify --key XXXX-XXXX-XXXX-XXXX
    python3 license.py list
    python3 license.py revoke --key XXXX-XXXX-XXXX-XXXX
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import secrets
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

DB = Path(__file__).parent.parent / "data" / "licenses.db"
SECRET = os.environ.get("LICENSE_SECRET", "change-me-in-production-set-env-var")


def _conn() -> sqlite3.Connection:
    DB.parent.mkdir(exist_ok=True)
    c = sqlite3.connect(DB)
    c.execute("""
        CREATE TABLE IF NOT EXISTS licenses (
            key TEXT PRIMARY KEY,
            email TEXT NOT NULL,
            plan TEXT NOT NULL,
            seats INTEGER NOT NULL DEFAULT 1,
            status TEXT NOT NULL DEFAULT 'active',
            stripe_id TEXT,
            created_at TEXT NOT NULL,
            notes TEXT
        )
    """)
    c.commit()
    return c


def _keygen() -> str:
    raw = secrets.token_hex(8).upper()
    return f"{raw[0:4]}-{raw[4:8]}-{raw[8:12]}-{raw[12:16]}"


def generate(email: str, plan: str, stripe_id: str | None = None, notes: str | None = None) -> str:
    key = _keygen()
    seats = 3 if plan == "firm" else 1
    c = _conn()
    c.execute(
        "INSERT INTO licenses VALUES (?,?,?,?,?,?,?,?)",
        (key, email.lower().strip(), plan, seats, "active", stripe_id,
         datetime.utcnow().isoformat(), notes),
    )
    c.commit()
    c.close()
    return key


def verify(key: str) -> dict | None:
    c = _conn()
    row = c.execute(
        "SELECT email, plan, seats, status, created_at FROM licenses WHERE key=?",
        (key.upper().strip(),),
    ).fetchone()
    c.close()
    if row is None:
        return None
    return {"email": row[0], "plan": row[1], "seats": row[2], "status": row[3], "created": row[4]}


def revoke(key: str) -> bool:
    c = _conn()
    c.execute("UPDATE licenses SET status='revoked' WHERE key=?", (key.upper().strip(),))
    changed = c.total_changes
    c.commit()
    c.close()
    return changed > 0


def list_all() -> list[dict]:
    c = _conn()
    rows = c.execute(
        "SELECT key, email, plan, seats, status, stripe_id, created_at FROM licenses ORDER BY created_at DESC"
    ).fetchall()
    c.close()
    return [
        {"key": r[0], "email": r[1], "plan": r[2], "seats": r[3],
         "status": r[4], "stripe_id": r[5], "created": r[6]}
        for r in rows
    ]


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")

    g = sub.add_parser("generate")
    g.add_argument("--email", required=True)
    g.add_argument("--plan", choices=["solo", "firm", "early_bird"], default="solo")
    g.add_argument("--stripe-id")
    g.add_argument("--notes")

    v = sub.add_parser("verify")
    v.add_argument("--key", required=True)

    sub.add_parser("list")

    r = sub.add_parser("revoke")
    r.add_argument("--key", required=True)

    args = ap.parse_args()
    if not args.cmd:
        ap.print_help()
        return 1

    if args.cmd == "generate":
        key = generate(args.email, args.plan, getattr(args, "stripe_id", None), getattr(args, "notes", None))
        print(f"Key: {key}")
        print(f"Email: {args.email}  Plan: {args.plan}")
    elif args.cmd == "verify":
        info = verify(args.key)
        if info is None:
            print("INVALID — key not found")
            return 1
        if info["status"] != "active":
            print(f"INVALID — key {info['status']}")
            return 1
        print(f"VALID  {info['plan'].upper()} | {info['email']} | {info['seats']} seat(s)")
    elif args.cmd == "list":
        rows = list_all()
        if not rows:
            print("No licenses yet.")
        for r in rows:
            print(f"[{r['status']:8}] {r['key']}  {r['plan']:10} {r['email']}")
    elif args.cmd == "revoke":
        ok = revoke(args.key)
        print("Revoked." if ok else "Key not found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
