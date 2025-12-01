#!/bin/bash 
set -euo pipefail

# -------- Configuration & helpers --------
DEFAULT_PARALLEL=10
CURL_TIMEOUT=10    # seconds
TMPDIR=$(mktemp -d)
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
CSV_FILE="website_report_${TIMESTAMP}.csv"
HTML_FILE="website_report_${TIMESTAMP}.html"
SUMMARY_FILE="website_report_summary_${TIMESTAMP}.txt"

RED='\033[0;31m'
YELLOW='\033[0;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

cleanup() {
    rm -rf "$TMPDIR"
}
trap cleanup EXIT

usage() {
    cat <<EOF
Usage: $0 -f sites.txt [-p parallel] [-e email]

Options:
  -f FILE      File containing websites/URLs (one per line). Required.
  -p N         Parallel workers for checking (default: $DEFAULT_PARALLEL)
  -e EMAIL     Email address to notify if any site is DOWN (optional)
  -h           Show this help
EOF
    exit 1
}

# -------- Parse args --------
PARALLEL=$DEFAULT_PARALLEL
EMAIL=""
