#!/usr/bin/env python3
"""Filter and rank fetched grants against a writer profile.

Inputs raw fetch JSON, scores each opportunity, emits a ranked shortlist with
a deterministic "why this fits" string per hit.

Usage:
    python3 rank.py --profile ../config/profile.json --raw ../data/raw.json --out ../data/ranked.json
"""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime
from pathlib import Path
from typing import Any


def parse_date(s: str | None) -> date | None:
    if not s:
        return None
    for fmt in ("%m/%d/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def days_until(close: str | None, today: date) -> int | None:
    d = parse_date(close)
    if d is None:
        return None
    return (d - today).days


def score_and_explain(
    hit: dict[str, Any], profile: dict[str, Any], today: date
) -> tuple[float, list[str]]:
    score = 0.0
    reasons: list[str] = []

    title = (hit.get("title") or "").lower()
    desc = (hit.get("description") or "").lower()
    agency = (hit.get("agencyCode") or "").upper()
    alns = [a for a in (hit.get("cfdaList") or hit.get("alnist") or []) if a]

    keywords = profile.get("keywords") or []
    title_kw_hits = [k for k in keywords if k.lower() in title]
    if title_kw_hits:
        score += 3 * len(title_kw_hits)
        reasons.append(f"title matches keywords: {', '.join(title_kw_hits)}")
    if desc:
        desc_kw_hits = [k for k in keywords if k.lower() in desc and k not in title_kw_hits]
        if desc_kw_hits:
            score += 1 * len(desc_kw_hits)
            reasons.append(f"description matches keywords: {', '.join(desc_kw_hits)}")

    pref_agencies = {a.upper() for a in (profile.get("preferred_agencies") or [])}
    if agency in pref_agencies:
        score += 2
        reasons.append(f"preferred agency ({agency})")

    pref_alns = set(profile.get("preferred_alns") or [])
    aln_match = pref_alns.intersection(alns)
    if aln_match:
        score += 4
        reasons.append(f"matches ALN(s): {', '.join(sorted(aln_match))}")

    excluded_kws = [
        k for k in (profile.get("exclude_keywords") or [])
        if k.lower() in title or (desc and k.lower() in desc)
    ]
    if excluded_kws:
        score -= 5
        reasons.append(f"contains excluded terms: {', '.join(excluded_kws)}")

    award_min = profile.get("min_award_amount")
    award_max = profile.get("max_award_amount")
    ceiling = hit.get("awardCeiling")
    floor = hit.get("awardFloor")
    if ceiling or floor:
        size = ceiling or floor
        if award_min and size and size < award_min:
            score -= 4
            reasons.append(f"award size ${size:,} below ${award_min:,} floor")
        elif award_max and size and size > award_max:
            score -= 1
            reasons.append(f"award size ${size:,} above ${award_max:,} ceiling")
        else:
            reasons.append(
                f"award ${floor:,}–${ceiling:,}" if floor and ceiling
                else f"award up to ${ceiling:,}" if ceiling
                else f"award from ${floor:,}"
            )

    dleft = days_until(hit.get("closeDate"), today)
    min_days = profile.get("min_days_until_deadline", 14)
    max_days = profile.get("max_days_until_deadline")
    if dleft is not None:
        if dleft < min_days:
            score -= 3
            reasons.append(f"only {dleft}d to deadline (under {min_days}d threshold)")
        elif max_days and dleft > max_days:
            score -= 1
            reasons.append(f"{dleft}d to deadline (beyond {max_days}d window)")
        else:
            score += 1
            reasons.append(f"{dleft}d to deadline")
    else:
        if (hit.get("oppStatus") or "").lower() == "forecasted":
            reasons.append("forecasted (no close date yet)")

    return score, reasons


def rank(profile: dict[str, Any], raw: dict[str, Any]) -> list[dict[str, Any]]:
    today = date.today()
    out: list[dict[str, Any]] = []
    for hit in raw.get("oppHits", []):
        score, reasons = score_and_explain(hit, profile, today)
        if score < profile.get("min_score", 1):
            continue
        out.append(
            {
                "id": hit.get("id"),
                "number": hit.get("number"),
                "title": hit.get("title"),
                "agency": hit.get("agency") or hit.get("agencyName"),
                "agencyCode": hit.get("agencyCode"),
                "openDate": hit.get("openDate"),
                "closeDate": hit.get("closeDate"),
                "status": hit.get("oppStatus"),
                "alns": hit.get("cfdaList") or hit.get("alnist") or [],
                "awardCeiling": hit.get("awardCeiling"),
                "awardFloor": hit.get("awardFloor"),
                "estimatedFunding": hit.get("estimatedFunding"),
                "url": f"https://www.grants.gov/search-results-detail/{hit.get('id')}",
                "score": round(score, 2),
                "why": reasons,
            }
        )
    out.sort(key=lambda r: r["score"], reverse=True)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", required=True)
    ap.add_argument("--raw", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--limit", type=int, default=25)
    args = ap.parse_args()

    profile = json.loads(Path(args.profile).read_text())
    raw = json.loads(Path(args.raw).read_text())
    ranked = rank(profile, raw)[: args.limit]
    Path(args.out).write_text(json.dumps(ranked, indent=2))
    print(f"Ranked {len(ranked)} opportunities -> {args.out}")
    for r in ranked[:10]:
        print(f"  [{r['score']:>4}] {r['title'][:80]} ({r['agencyCode']}, closes {r['closeDate'] or 'TBD'})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
