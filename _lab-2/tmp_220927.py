from functools import reduce

data_ = []
for l in open('flavors_of_cacao.csv').readlines()[1:]:
    data_.append(l.split(',')[5])

# mapper
# convert list of countries to list of tuples with '1' near each country
data = list(map(lambda x: (x, 1), data_))

# merge-sort
data.sort()

# reduce
# summarize all numeric fields for each instance
# 1. сделать это с использованием множества (set)
# 2. с использованием словаря (dict)
# 3. потоком
"""
last_el = data[0][0]
d = {data[0][0]: 0}
for e, _ in data:
    if e == last_el:
        d[e] += 1
    else:
        last_el = e
        d[e] = 1

print(d)
"""
# 4. используя reduce
# 5. разделяя списки
d = {}
unq = set(data_)
for e in unq:
    d[e] = reduce(lambda x, y: x[1] + y[1] if x[0] == e else x[1], data)
print(d)

# 6. за один проход по списку
"""
i = 0
d = {}
data_.sort()
while i < len(data_):
    d[data_[i]] = data.count(data[i])
    i += data.count(data[i])
print(d)
"""
