#!/bin/bash
# Daily grants-scan runner — invoked by LaunchAgent or cron.
# Results go to data/ranked.json. Optionally posts a digest email.

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG="$DIR/data/daily-scan.log"
PROFILE="$DIR/config/profile.json"

if [ ! -f "$PROFILE" ]; then
    echo "$(date): No profile.json found at $PROFILE — skipping" >> "$LOG"
    exit 0
fi

echo "$(date): Starting daily scan..." >> "$LOG"

cd "$DIR"
python3 scripts/grants_fetch.py --profile "$PROFILE" --out data/raw.json     >> "$LOG" 2>&1
python3 scripts/enrich.py --raw data/raw.json --profile "$PROFILE" --out data/enriched.json --top-k 50  >> "$LOG" 2>&1
python3 scripts/rank.py --profile "$PROFILE" --raw data/enriched.json --out data/ranked.json --limit 15 >> "$LOG" 2>&1

echo "$(date): Done." >> "$LOG"
