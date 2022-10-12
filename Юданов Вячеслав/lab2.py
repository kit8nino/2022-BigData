from cProfile import label
from collections import Counter
from functools import reduce
import csv
data_ = []
with open('./_lab-2/flavors_ofcacao.csv',newline='') as f:
    reader = csv.DictReader(f)
    for i in reader:
        data.append(i['Company Location'])
res = Counter(data)
print(dict(res))
data = []
with open('./_lab-2/flavors_of_cacao2.csv',)as file:
    reader = csv.reader(file)
    for i in reader:
        data.append(i[5])
res = Counter(data_)
print(dict(res)) 