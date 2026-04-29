#!/usr/bin/env python3
"""Fetch open opportunities from grants.gov search2 API.

Stdlib only. No API key required.

Usage:
    python3 grants_fetch.py --profile ../config/profile.json --out ../data/raw.json
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path
from typing import Any

API_URL = "https://api.grants.gov/v1/api/search2"
DEFAULT_ROWS = 200
USER_AGENT = "grant-writer-pack/0.1 (+https://github.com/)"


def post_search(body: dict[str, Any], timeout: float = 30.0) -> dict[str, Any]:
    payload = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=payload,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def build_body(profile: dict[str, Any]) -> dict[str, Any]:
    body: dict[str, Any] = {
        "rows": profile.get("rows", DEFAULT_ROWS),
        "oppStatuses": profile.get("oppStatuses", "forecasted|posted"),
    }
    for key in ("keyword", "agencies", "fundingCategories", "aln", "eligibilities"):
        val = profile.get(key)
        if val:
            body[key] = val
    return body


def fetch(profile: dict[str, Any]) -> dict[str, Any]:
    keywords = profile.get("keywords") or [profile.get("keyword", "")]
    keywords = [k for k in keywords if k]
    if not keywords:
        keywords = [""]

    seen_ids: set[str] = set()
    merged_hits: list[dict[str, Any]] = []
    for kw in keywords:
        body = build_body({**profile, "keyword": kw})
        result = post_search(body)
        if result.get("errorcode", 0) != 0:
            print(f"[warn] search failed for keyword={kw!r}: {result.get('msg')}", file=sys.stderr)
            continue
        hits = (result.get("data") or {}).get("oppHits") or []
        for hit in hits:
            hid = hit.get("id")
            if hid and hid not in seen_ids:
                seen_ids.add(hid)
                merged_hits.append(hit)

    return {"hitCount": len(merged_hits), "oppHits": merged_hits}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", required=True, help="Path to profile JSON")
    ap.add_argument("--out", required=True, help="Where to write raw fetch results")
    args = ap.parse_args()

    profile = json.loads(Path(args.profile).read_text())
    data = fetch(profile)
    Path(args.out).write_text(json.dumps(data, indent=2))
    print(f"Fetched {data['hitCount']} opportunities -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
