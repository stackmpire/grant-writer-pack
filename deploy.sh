#!/bin/bash
# One-shot deploy: authenticate, create GitHub repo, push, enable Pages.
# Run this once: bash deploy.sh

set -e
BLUE="\033[0;34m"; GREEN="\033[0;32m"; YELLOW="\033[1;33m"; RESET="\033[0m"

REPO_NAME="grant-writer-pack"
PAGES_BRANCH="main"

echo -e "${BLUE}Grant Writer Pack — deploy script${RESET}"
echo ""

# 1 — gh auth
if ! gh auth status &>/dev/null; then
    echo -e "${YELLOW}Step 1: Log in to GitHub (browser will open)${RESET}"
    gh auth login --web --git-protocol https
else
    GH_USER=$(gh api user --jq .login)
    echo -e "  GitHub: logged in as ${GREEN}$GH_USER${RESET}"
fi

GH_USER=$(gh api user --jq .login)

# 2 — create repo if needed
if gh repo view "$GH_USER/$REPO_NAME" &>/dev/null; then
    echo -e "  Repo:   ${GREEN}$GH_USER/$REPO_NAME already exists${RESET}"
else
    echo -e "${YELLOW}Step 2: Creating GitHub repo...${RESET}"
    gh repo create "$REPO_NAME" --public \
        --description "A Claude Code plugin for solo grant writers — daily grants.gov scanner, RFP drafter, boilerplate vault" \
        --source . \
        --remote origin \
        --push
    echo -e "  Repo:   ${GREEN}https://github.com/$GH_USER/$REPO_NAME${RESET}"
fi

# 3 — set remote + push
if ! git remote get-url origin &>/dev/null; then
    git remote add origin "https://github.com/$GH_USER/$REPO_NAME.git"
fi

git add -A
git diff --cached --quiet || git commit -m "Initial release v0.1"
git push -u origin main 2>/dev/null || git push -u origin master 2>/dev/null || true

# 4 — update placeholders in source files
echo -e "\n${YELLOW}Updating repo URL placeholders...${RESET}"
REPO_URL="https://github.com/$GH_USER/$REPO_NAME"
RAW_INSTALL="https://raw.githubusercontent.com/$GH_USER/$REPO_NAME/main/install.sh"
sed -i '' "s|YOUR_USERNAME|$GH_USER|g" \
    install.sh \
    scripts/provision.py \
    marketing/emails/welcome.txt \
    marketing/landing.html \
    CLAUDE.md 2>/dev/null || true
git add -A
git diff --cached --quiet || git commit -m "Set GitHub username in URLs"
git push 2>/dev/null || true

# 5 — enable GitHub Pages
echo -e "\n${YELLOW}Enabling GitHub Pages (marketing/ folder)...${RESET}"
# Rename landing.html -> index.html for Pages
cp marketing/landing.html marketing/index.html
git add marketing/index.html
git diff --cached --quiet || git commit -m "Add marketing/index.html for GitHub Pages"
git push 2>/dev/null || true

gh api "repos/$GH_USER/$REPO_NAME/pages" \
    --method POST \
    --field source='{"branch":"main","path":"/marketing"}' \
    2>/dev/null && echo -e "  Pages:  ${GREEN}enabled${RESET}" || \
    echo -e "  Pages:  already enabled or needs manual setup at github.com/$GH_USER/$REPO_NAME/settings/pages"

PAGES_URL="https://$GH_USER.github.io/$REPO_NAME"

# 6 — summary
echo ""
echo -e "${GREEN}Done.${RESET}"
echo ""
echo "  Repo:      https://github.com/$GH_USER/$REPO_NAME"
echo "  Landing:   $PAGES_URL  (live in ~60 seconds)"
echo "  Install:   git clone https://github.com/$GH_USER/$REPO_NAME.git"
echo ""
echo -e "${YELLOW}Next 3 steps to take money:${RESET}"
echo "  1. Create a Stripe account at https://stripe.com"
echo "     Then open marketing/checkout.html and paste your publishable key."
echo ""
echo "  2. Set your email for license delivery:"
echo "     export SMTP_USER=you@gmail.com"
echo "     export SMTP_PASS=your-gmail-app-password"
echo "     (Get an app password at https://myaccount.google.com/apppasswords)"
echo ""
echo "  3. Post to r/grantwriting using marketing/reddit-launch-post.md"
echo "     and send 10 cold emails using marketing/cold-emails.md"
echo ""
echo "  To provision a customer manually after they pay:"
echo "    python3 scripts/provision.py --email THEIR_EMAIL --plan solo"
echo ""
