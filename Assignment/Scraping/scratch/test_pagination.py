import urllib.request
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def check_page(page_num):
    url = f"https://sourcing.alibaba.com/rfq/rfq_search_list.htm?country=AE&recently=Y&tracelog=newest&page={page_num}"
    req = urllib.request.Request(url, headers=headers)
    html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
    matches = re.findall(r'window\.PAGE_DATA\["index"\]\.data\.push\((\{.*?\}\s*)\);', html, re.DOTALL)
    
    # Also check pagination data in window.PAGE_DATA["index"] if any
    total_page_match = re.search(r'totalPage\s*:\s*(\d+)', html)
    total_count_match = re.search(r'totalCount\s*:\s*(\d+)', html)
    total_page = total_page_match.group(1) if total_page_match else "N/A"
    total_count = total_count_match.group(1) if total_count_match else "N/A"
    
    print(f"Page {page_num}: found {len(matches)} RFQs. totalPage: {total_page}, totalCount: {total_count}")
    return len(matches)

for p in range(1, 10):
    count = check_page(p)
    if count == 0:
        break
