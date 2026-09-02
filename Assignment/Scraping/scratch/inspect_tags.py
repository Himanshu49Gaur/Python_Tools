import re
import json

with open('scratch/page.html', 'r', encoding='utf-8') as f:
    html = f.read()

pattern = r'window\.PAGE_DATA\["index"\]\.data\.push\((\{.*?\}\s*)\);'
matches = re.findall(pattern, html, re.DOTALL)

tags_seen = set()
for m in matches:
    # Find tags: [...]
    tag_match = re.search(r'tags:\s*(\[.*?\])\s*\|\|', m, re.DOTALL)
    if tag_match:
        tag_str = tag_match.group(1)
        # convert JS hex escapes
        tag_str = re.sub(r'\\x([0-9a-fA-F]{2})', lambda x: chr(int(x.group(1), 16)), tag_str)
        # simple quote keys for json
        tag_str = re.sub(r'([a-zA-Z0-9_]+)\s*:', r'"\1":', tag_str)
        try:
            t_list = json.loads(tag_str)
            for t in t_list:
                tags_seen.add((t.get('tagName'), t.get('type'), t.get('scene')))
        except Exception as e:
            print("Error parsing tags:", e, tag_str)

print("All tags found on page 1:")
for t in sorted(tags_seen):
    print(t)
