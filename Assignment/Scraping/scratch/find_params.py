import re

with open('scratch/page.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Search for totalPage, totalCount, pageNo, etc.
for match in re.finditer(r'(totalPage|totalCount|total|pageSize|page|pageNo)\s*[:=]\s*([^,;}\n]+)', html, re.IGNORECASE):
    print(match.group(1), ":", match.group(2))
