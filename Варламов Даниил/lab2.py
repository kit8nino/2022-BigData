from cProfile import label
from collections import Counter
from functools import reduce
import csv
data_ = []
with open('./_lab-2/flavors_of_cacao.csv',newline='') as f:
    reader = csv.DictReader(f)
    for i in reader:
        data_.append(i['Company Location'])
res = Counter(data_)
print(dict(res))
data_ = []
with open('./_lab-2/flavors_of_cacao_2.csv',)as file:
    reader = csv.reader(file)
    for i in reader:
        data_.append(i[5])
res = Counter(data_)
print(dict(res))