from functools import reduce
from collections import Counter

data1 = []
for l in open('flavors_of_cacao.csv').readlines()[1:]:
    data1.append(l.split(',')[5])
 
data2 = []
for l in open('flavors_of_cacao_2.csv').readlines()[1:]:
    data2.append(l.split(',')[5])

res = data1 + data2
data = list(map(lambda x:(x),res))
data.sort()
res = Counter(data)
print(res)