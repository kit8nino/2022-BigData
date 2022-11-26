import csv
from collections import Counter


def countryCounter(file):

    with open(file, "r", encoding="utf-8", newline="") as csv_file:
        out = [row[5] for row in csv.reader(csv_file)]
        return out

if __name__ == '__main__':
    _countries = countryCounter('cacao.csv') + countryCounter('cacao_2.csv')
    _countries.sort()
    print(dict(Counter(_countries)))



