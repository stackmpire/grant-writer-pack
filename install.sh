#!/bin/bash
# Grant Writer Pack — one-line customer installer
#
# Usage:
#   curl -sSL https://raw.githubusercontent.com/stackmpire/grant-writer-pack/main/install.sh | bash
#
# Or clone manually:
#   git clone https://github.com/stackmpire/grant-writer-pack.git
#   cd grant-writer-pack && bash install.sh

set -e

REPO="https://github.com/stackmpire/grant-writer-pack.git"
INSTALL_DIR="$HOME/grant-writer-pack"
BLUE="\033[0;34m"; GREEN="\033[0;32m"; RESET="\033[0m"; RED="\033[0;31m"

echo -e "${BLUE}Grant Writer Pack installer${RESET}"
echo ""

# 1 — Python check
if ! command -v python3 &>/dev/null; then
    echo -e "${RED}Error: python3 is required. Install from https://python.org${RESET}"
    exit 1
fi

PY=$(python3 --version 2>&1 | awk '{print $2}')
echo "  python3 $PY — OK"

# 2 — Claude Code check
if ! command -v claude &>/dev/null; then
    echo -e "${RED}Error: Claude Code CLI is required.${RESET}"
    echo "  Install: https://claude.ai/code"
    exit 1
fi
echo "  Claude Code — OK"

# 3 — Clone or update
if [ -d "$INSTALL_DIR/.git" ]; then
    echo -e "\n  Updating existing install at $INSTALL_DIR..."
    git -C "$INSTALL_DIR" pull --quiet
else
    echo -e "\n  Cloning to $INSTALL_DIR..."
    git clone --quiet "$REPO" "$INSTALL_DIR"
fi

cd "$INSTALL_DIR"

# 4 — Profile setup
if [ ! -f config/profile.json ]; then
    cp config/profile.example.json config/profile.json
    echo ""
    echo -e "${BLUE}Profile created at config/profile.json${RESET}"
    echo "  Edit it before running /grants-scan:"
    echo "    keywords       — phrases to match in opportunity titles"
    echo "    preferred_agencies — agency codes: HHS, ED, USDA, DOJ, etc."
    echo "    preferred_alns — CFDA/ALN numbers for your niche"
else
    echo "  Profile already exists — not overwritten"
fi

# 5 — Boilerplate directory
mkdir -p boilerplate drafts data

# 6 — Done
echo ""
echo -e "${GREEN}Install complete.${RESET}"
echo ""
echo "  Next steps:"
echo "  1. Edit config/profile.json with your keywords + agencies"
echo "  2. Open this folder in Claude Code:   claude $INSTALL_DIR"
echo "  3. Type /grants-scan"
echo ""
echo "  Drop past proposals into boilerplate/ as .txt or .md files"
echo "  to unlock /grants-boilerplate"
echo ""
echo "  Questions? hello@grantwriterpack.com"
