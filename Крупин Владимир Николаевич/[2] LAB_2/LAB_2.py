import csv
import glob
from collections import Counter
COUNTRIES = []
for i in glob.glob("*.csv"):
    with open(i, "r", encoding="utf-8", newline="") as file:
        COUNTRIES += [row[5] for row in csv.reader(file)]
COUNTRIES.sort()
print("\nRESULT: ", dict(Counter(COUNTRIES)))
