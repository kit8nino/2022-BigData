from functools import reduce

data_ = []
for l in open('flavors_of_cacao.csv').readlines()[1:]:
    data_.append(l.split(',')[5])
data1= []
for i in open('flavors_of_cacao_2.csv').readlines()[1:]:
    data1.append(i.split(',')[5])
res = []
res = data1 + data_
# mapper
# convert list of countries to list of tuples with '1' near each country
data = list(map(lambda x: (x, 1), res))
# merge-sort
data.sort()

# reduce
# summarize all numeric fields for each instance

# 6. за один проход по списку
i = 0
d2 = {}
while i < len(res):
    d2[res[i]] = data.count(data[i])
    i += data.count(data[i])
print(d2)
