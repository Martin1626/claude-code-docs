import zipfile
import re

path = r"C:\Git\alzask\docs\onboarding\prezentace-01-uvod-a-zakladni-kolobeh-predprijem.pptx"
z = zipfile.ZipFile(path)
slide_files = sorted([n for n in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$', n)],
                      key=lambda n: int(re.search(r'\d+', n).group()))
print("Slide count:", len(slide_files))
for sf in slide_files:
    xml = z.read(sf).decode('utf-8')
    texts = re.findall(r'<a:t>(.*?)</a:t>', xml)
    joined = ' '.join(texts).strip()
    print(f"--- {sf} ---")
    print(joined[:500])
