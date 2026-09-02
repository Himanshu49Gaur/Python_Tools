import urllib.request
import re
import sys

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def get_page_rfqs(page_num):
    url = f"https://sourcing.alibaba.com/rfq/rfq_search_list.htm?country=AE&recently=Y&tracelog=newest&page={page_num}"
    req = urllib.request.Request(url, headers=headers)
    try:
        html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Page {page_num} fetch error: {e}", flush=True)
        return []
    
    matches = re.findall(r'window\.PAGE_DATA\["index"\]\.data\.push\((\{.*?\}\s*)\);', html, re.DOTALL)
    print(f"Page {page_num}: found {len(matches)} RFQs", flush=True)
    if matches:
        # extract id from first item
        id_match = re.search(r'id:\s*"(\d+)"', matches[0])
        first_id = id_match.group(1) if id_match else "N/A"
        print(f"  First RFQ ID on page {page_num}: {first_id}", flush=True)
    return matches

for p in range(1, 5):
    rfqs = get_page_rfqs(p)
    if not rfqs:
        break
