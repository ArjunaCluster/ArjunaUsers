#!/bin/bash
# Script to update usage pages and push the results

# Locate the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PKG_ROOT=$(dirname $SCRIPT_DIR)
cd "$PKG_ROOT"

# Update repo
git fetch origin
git pull --rebase origin main
git checkout -b weekly_usage

# Update stats
make install
mkdir -p _includes
mkdir -p img
python3 dev/usage_stats.py

# Commit results
git add _includes/user_stats.md img/weekly_usage.png
git commit -m"Update Weekly Stats"
git push -u origin weekly_usage

# Clean up
git branch -D weekly_usage
