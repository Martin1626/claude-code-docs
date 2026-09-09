#!/usr/bin/env python3
"""Srovná pořadí sekcí 2 a 3 ve faze3a-alzask-metodiky.md (sekce 2 byla appendována za 3)."""
import io
import sys

PATH = r"C:\tmp\workshop-namety\_raw\faze3a-alzask-metodiky.md"

with io.open(PATH, "r", encoding="utf-8") as fh:
    lines = fh.readlines()


def find(prefix):
    for i, line in enumerate(lines):
        if line.startswith(prefix):
            return i
    raise SystemExit("nenalezeno: " + prefix)


i3 = find("## 3. ")
i2 = find("## 2. ")
i4 = find("## 4. ")

if not (i3 < i2 < i4):
    print("Poradi uz je v poradku nebo neocekavane; nic nemenim.")
    sys.exit(0)

# blok sekce 3 = [i3, i2), blok sekce 2 = [i2, i4)
# oddelovac "---" patri pred kazdy nadpis; bloky konci prazdnym radkem + '---'
sec3 = lines[i3:i2]
sec2 = lines[i2:i4]

lines[i3:i4] = sec2 + sec3

with io.open(PATH, "w", encoding="utf-8", newline="") as fh:
    fh.writelines(lines)

print("Prehozeno: sekce 2 (%d radku) nyni pred sekci 3 (%d radku)." % (len(sec2), len(sec3)))
