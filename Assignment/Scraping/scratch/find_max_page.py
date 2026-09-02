import urllib.request
import re

url = "https://sourcing.alibaba.com/rfq/rfq_search_list.htm?country=AE&recently=Y&tracelog=newest"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, Gecko) Chrome/120.0.0.0 Safari/537.36'}
req = urllib.request.Request(url, headers=headers)
html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')

# Find page links in html
page_numbers = re.findall(r'page\s*=\s*(\d+)', html)
print("Page numbers found in links:", sorted(set(map(int, page_numbers))))

# Find pagination div/nav HTML snippet
nav_match = re.search(r'<div[^>]*class="[^"]*ui-pagination[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL)
if nav_match:
    print("Pagination nav HTML:")
    print(nav_match.group(0)[:500])

# Check window.PAGE_DATA["index"] properties
idx_data = re.search(r'window\.PAGE_DATA\["index"\]\s*=\s*(\{.*?\});', html, re.DOTALL)
if idx_data:
    print("Index data:", idx_data.group(1))
