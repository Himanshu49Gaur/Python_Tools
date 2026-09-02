import re

with open('scratch/page.html', 'r', encoding='utf-8') as f:
    html = f.read()

pattern = r'window\.PAGE_DATA\["index"\]\.data\.push\((\{.*?\}\s*)\);'
matches = re.findall(pattern, html, re.DOTALL)

if matches:
    print("=== FULL OBJECT 0 ===")
    print(matches[0])
