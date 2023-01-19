import csv
from collections import Counter
from pprint import pprint

result = []

with open("flavors_of_cacao.csv") as f1, open("flavors_of_cacao_2.csv") as f2:
    file_reader_1 = csv.reader(f1)
    file_reader_2 = csv.reader(f2)
    result += [row[5] for row in file_reader_1]
    result += [row[5] for row in file_reader_2]

pprint(dict(Counter(result)))