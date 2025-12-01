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

while getopts ":f:p:e:h" opt; do
  case ${opt} in
    f ) SITES_FILE=$OPTARG ;;
    p ) PARALLEL=$OPTARG ;;
    e ) EMAIL=$OPTARG ;;
    h ) usage ;;
    \? ) echo "Invalid Option: -$OPTARG" >&2; usage ;;
    : ) echo "Invalid Option: -$OPTARG requires an argument" >&2; usage ;;
  esac
done

if [[ -z "${SITES_FILE:-}" ]]; then
    echo "Error: sites file required."
    usage
fi

if [[ ! -f "$SITES_FILE" ]]; then
    echo "Error: File '$SITES_FILE' not found."
    exit 2
fi

# check mail command presence if EMAIL provided
if [[ -n "$EMAIL" ]]; then
    if ! command -v mail >/dev/null 2>&1; then
        echo -e "${YELLOW}Warning:${NC} 'mail' command not found. Email notification will be skipped."
        EMAIL=""
    fi
fi

echo "Starting Website Status Check"
echo "Sites file : $SITES_FILE"
echo "Parallel   : $PARALLEL"
[[ -n "$EMAIL" ]] && echo "Notify to  : $EMAIL"
echo "CSV output : $CSV_FILE"
echo "HTML output: $HTML_FILE"
echo ""

# -------- Prepare worker script --------
WORKER_SH="$TMPDIR/check_worker.sh"
cat > "$WORKER_SH" <<'WORKER'
#!/usr/bin/env bash
set -euo pipefail
site="$1"
CURL_TIMEOUT="$2"

# normalize: if no scheme, prepend http://
if [[ "$site" != http*://* ]]; then
  url="http://$site"
else
  url="$site"
fi

# Use curl to get status code and total time. If curl fails, return 000 and time 0
result=$(curl -s -o /dev/null -w "%{http_code} %{time_total}" --max-time "$CURL_TIMEOUT" "$url" 2>/dev/null) || result="000 0"
code=$(awk '{print $1}' <<< "$result")
time_total=$(awk '{print $2}' <<< "$result")
# trim
code=$(echo "$code")
time_total=$(echo "$time_total")

# Determine status string
if [[ "$code" == "000" ]]; then
  status="DOWN"
elif [[ "$code" -ge 200 && "$code" -lt 400 ]]; then
  status="UP"
else
  status="ERROR"
fi

# Print CSV line: site,code,time,status
printf '%s,%s,%s,%s\n' "$site" "$code" "$time_total" "$status"
WORKER
chmod +x "$WORKER_SH"

# -------- Run checks in parallel and collect results --------
# Create worklist with non-empty trimmed lines and ignoring comments
WORKLIST="$TMPDIR/worklist.txt"
grep -vE '^\s*$|^\s*#' "$SITES_FILE" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' > "$WORKLIST"

if [[ ! -s "$WORKLIST" ]]; then
    echo "No sites to check in $SITES_FILE"
    exit 0
fi

# Use xargs to run worker in parallel
# Each output line appended to tmp_results (order may vary)
TMP_RESULTS="$TMPDIR/results.unsorted.csv"
: > "$TMP_RESULTS"

export CURL_TIMEOUT

# xargs approach — one arg per line
# For portability, use bash -c wrapper to call worker script
cat "$WORKLIST" | xargs -P "$PARALLEL" -I {} bash -c '"'"$WORKER_SH"'" "{}" "'"$CURL_TIMEOUT"'"' >> "$TMP_RESULTS"

# sort results by site for stable output
sort "$TMP_RESULTS" > "$TMPDIR/results.sorted.csv"

# Produce final CSV with header
echo "site,http_code,response_time_seconds,status" > "$CSV_FILE"
cat "$TMPDIR/results.sorted.csv" >> "$CSV_FILE"

# -------- Terminal color-coded output and generate summary --------
DOWN_COUNT=0
UP_COUNT=0
ERROR_COUNT=0
echo "Live results:"
while IFS=, read -r site code time_total status; do
    if [[ "$status" == "UP" ]]; then
        echo -e "${GREEN}$site is UP | ${code} | ${time_total}s${NC}"
        ((UP_COUNT++))
    elif [[ "$status" == "ERROR" ]]; then
        echo -e "${YELLOW}$site has ERROR (code ${code}) | ${time_total}s${NC}"
        ((ERROR_COUNT++))
    else
        echo -e "${RED}$site is DOWN or unreachable${NC}"
        ((DOWN_COUNT++))
    fi
done < <(tail -n +1 "$CSV_FILE" | sed '1d')   # skip header

# -------- Summary & write human-readable summary --------
{
  echo "Website Status Report"
  echo "Generated: $(date)"
  echo "Total sites: $(wc -l < "$WORKLIST")"
  echo "UP: $UP_COUNT"
  echo "ERROR: $ERROR_COUNT"
  echo "DOWN: $DOWN_COUNT"
  echo ""

  echo ""
echo "Summary saved to $SUMMARY_FILE"
echo "CSV saved to $CSV_FILE"
  echo "Details (site,code,time,status):"
  tail -n +2 "$CSV_FILE"
} > "$SUMMARY_FILE"

