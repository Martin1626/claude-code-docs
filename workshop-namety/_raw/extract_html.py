import re
import html

path = r"C:\Git\shared\docs\claude-code\claude-code-jak-funguje.html"
with open(path, encoding='utf-8') as f:
    content = f.read()

print("=== FILE SIZE ===")
print(len(content), "chars")

# Extract title
m = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
if m:
    print("=== TITLE ===")
    print(html.unescape(m.group(1)).strip())

# Extract headings h1-h4
print("=== HEADINGS ===")
for m in re.finditer(r'<h([1-4])[^>]*>(.*?)</h\1>', content, re.IGNORECASE | re.DOTALL):
    level = m.group(1)
    text = re.sub(r'<[^>]+>', '', m.group(2))
    text = html.unescape(text).strip()
    text = re.sub(r'\s+', ' ', text)
    print(f"{'  ' * (int(level)-1)}H{level}: {text}")
