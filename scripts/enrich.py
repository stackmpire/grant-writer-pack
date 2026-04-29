#!/usr/bin/env python3
"""Enrich the top-K opportunities in raw.json with full detail data.

Pre-ranks all hits using rank.score_and_explain on title/agency/ALN, picks
the top K, fetches full detail (awardCeiling/Floor, synopsisDesc,
applicantEligibilityDesc), merges those fields back into each hit, and
writes a raw-shape JSON ready for a second pass through rank.py.

Usage:
    python3 enrich.py --raw ../data/raw.json --profile ../config/profile.json --out ../data/enriched.json
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path
from typing import Any

from rank import score_and_explain

DETAIL_URL = "https://api.grants.gov/v1/api/fetchOpportunity"
USER_AGENT = "grant-writer-pack/0.1"
SLEEP_BETWEEN = 0.2


def fetch_detail(opp_id: str, timeout: float = 15.0) -> dict[str, Any] | None:
    payload = json.dumps({"opportunityId": int(opp_id)}).encode("utf-8")
    req = urllib.request.Request(
        DETAIL_URL,
        data=payload,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
        print(f"[warn] detail fetch failed for {opp_id}: {e}", file=sys.stderr)
        return None
    if data.get("errorcode", 0) != 0:
        return None
    return (data.get("data") or {}).get("synopsis") or {}


def to_int(v: Any) -> int | None:
    if v in (None, "", 0, "0"):
        return None
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def merge_detail(hit: dict[str, Any], syn: dict[str, Any]) -> dict[str, Any]:
    out = dict(hit)
    out["awardCeiling"] = to_int(syn.get("awardCeiling"))
    out["awardFloor"] = to_int(syn.get("awardFloor"))
    out["estimatedFunding"] = to_int(syn.get("estimatedFunding"))
    out["expectedNumberOfAwards"] = to_int(syn.get("numberOfAwards"))
    out["description"] = (syn.get("synopsisDesc") or "")[:4000]
    out["eligibilityDesc"] = (syn.get("applicantEligibilityDesc") or "")[:2000]
    return out


def enrich(raw: dict[str, Any], profile: dict[str, Any], top_k: int) -> dict[str, Any]:
    hits = list(raw.get("oppHits", []))
    today = date.today()
    scored = sorted(
        hits,
        key=lambda h: score_and_explain(h, profile, today)[0],
        reverse=True,
    )
    to_enrich = scored[:top_k]
    rest = scored[top_k:]

    enriched: list[dict[str, Any]] = []
    for i, hit in enumerate(to_enrich):
        syn = fetch_detail(hit["id"])
        enriched.append(merge_detail(hit, syn) if syn else hit)
        if i + 1 < len(to_enrich):
            time.sleep(SLEEP_BETWEEN)

    return {"hitCount": len(enriched) + len(rest), "oppHits": enriched + rest}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", required=True)
    ap.add_argument("--profile", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--top-k", type=int, default=50)
    args = ap.parse_args()

    raw = json.loads(Path(args.raw).read_text())
    profile = json.loads(Path(args.profile).read_text())
    enriched = enrich(raw, profile, args.top_k)
    Path(args.out).write_text(json.dumps(enriched, indent=2))
    print(f"Enriched top {args.top_k} of {enriched['hitCount']} -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
