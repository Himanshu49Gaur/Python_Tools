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
