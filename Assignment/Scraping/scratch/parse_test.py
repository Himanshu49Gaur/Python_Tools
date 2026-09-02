import re

with open('scratch/page.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Look for script 29 or text containing window.PAGE_DATA["index"].data.push
start_idx = html.find('window.PAGE_DATA["index"].data.push(')
print("Start idx:", start_idx)

if start_idx != -1:
    snippet = html[start_idx:start_idx+2000]
    print("Snippet:")
    print(repr(snippet))
