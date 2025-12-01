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

