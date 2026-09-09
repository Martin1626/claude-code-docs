import re
import html

path = r"C:\Git\shared\docs\claude-code\claude-code-jak-funguje.html"
with open(path, encoding='utf-8') as f:
    content = f.read()

# strip script/style blocks
content = re.sub(r'<script.*?</script>', '', content, flags=re.IGNORECASE | re.DOTALL)
content = re.sub(r'<style.*?</style>', '', content, flags=re.IGNORECASE | re.DOTALL)

# convert block tags to newlines
content = re.sub(r'<(p|div|h[1-6]|li|br|section|article)[^>]*>', '\n', content, flags=re.IGNORECASE)
text = re.sub(r'<[^>]+>', '', content)
text = html.unescape(text)
# collapse whitespace per line
lines = [re.sub(r'[ \t]+', ' ', l).strip() for l in text.split('\n')]
lines = [l for l in lines if l]

out_path = r"C:\tmp\workshop-namety\_raw\claude-code-jak-funguje.stripped.txt"
with open(out_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print("Lines:", len(lines))
print("Chars:", sum(len(l) for l in lines))
print("Saved to", out_path)
