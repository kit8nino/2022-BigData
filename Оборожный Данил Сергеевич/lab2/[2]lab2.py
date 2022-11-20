import csv
import glob, os
from collections import Counter


if __name__ == "__main__":

    part = []

    for fileName in glob.glob("*.csv"):
        with open(fileName, "r", encoding="utf-8", newline="") as file:
            part += [row[5] for row in csv.reader(file)]
    
    _countries = part
    _countries.sort()

    data2 = dict(Counter(_countries))
    print(f"{data2=}")
