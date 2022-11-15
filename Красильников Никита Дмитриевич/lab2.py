from collections import Counter
import csv
data_ = []
with open('./_lab-2/flavors_of_cacao.csv') as file:
    reader = csv.DictReader(file)
    for i in reader:
        data_.append(i["Company Location"])
res = Counter(data_)
print(dict(res))

data_ = []
with open('./_lab-2/flavors_of_cacao_2.csv')as file:
    reader = csv.reader(file)
    for i in reader:
        data_.append(i[5])
res = Counter(data_)
print(dict(res))