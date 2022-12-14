from ast import Lambda
from collections import Counter
import csv
data=[]
data_ = []
with open("data.csv", "r", encoding="utf-8", newline="") as file:
    reader = csv.DictReader(file)
    for i in reader:
        data_.append(i['Company Location'])
res = Counter(data_)
print("\ntable1")
print(dict(res))
data1_ = []
with open("data1.csv", "r", encoding="utf-8", newline="") as file:
    reader = csv.reader(file)
    for i in reader:
        data1_.append(i[5])
res = Counter(data1_)
print("\ntable2")
print(dict(res))

data=data_+data1_
print("\nsumma 2 table")
res = Counter(data)
print(dict(res))
