from cProfile import label
from collections import Counter
from functools import reduce
import csv
data = []
with open('./_lab-2/flavors_of_cacao.csv',newline='') as f:
    reader = csv.DictReader(f)
    for i in reader:
        data.append(i['Company Location'])
result = Counter(data)
print(dict(result))
data = []
with open('./_lab-2/flavors_of_cacao_2.csv',)as file:
    reader = csv.reader(file)
    for i in reader:
        data.append(i[5])
result = Counter(data)
print(dict(result))