from functools import reduce

data_ = []
data__ = []

for l in open('flavors_of_cacao.csv').readlines()[1:]:
    data_.append(l.split(',')[5])

for l in open('flavors_of_cacao_2.csv').readlines()[1:]:
    data__.append(l.split(',')[5])

data_ += data__
data = list(map(lambda x: (x, 1), data_))
data.sort()
i = 0
d = {}
data_.sort()
while i < len(data_):
    d[data_[i]] = data.count(data[i])
    i += data.count(data[i])
print(d)