from collections import Counter
from pathlib import Path
import csv


def countries(*_files: str) -> dict:
    lines = []
    for file in _files:
        lines.extend(Path(file).read_text().split("\n"))

    reader = csv.reader(lines, delimiter=",", quotechar='"')

    all_countries = Counter([line[5] for line in reader])
    return dict(all_countries)


if __name__ == '__main__':
    files = ("flavors.csv", "flavors.csv")
    result = countries(*files)
    print(result)

