from functools import reduce
import numpy as np
import pandas as pd
#import itertools

data_ = []

m = []
mapped = open('words.csv', 'w', encoding='utf8')

for l in open(r'..\lab3\data.csv', 'r', encoding="utf8").readlines()[1:]:
    data_.append(l.split(',')[0]) 
for w in data_:
    words = w.split(' ')
    for u in words:
        m.append(u)
        mapped.write(u + '\n')
mapped.close()

res = [] 
for r in open('words.csv', 'r', encoding='utf8').readlines():
    res.append(r.split('\n')[0])

res = tuple(res)

data = list(map(lambda x: (x, 1), res))
data.sort()

i = 0
d = {}

while i < len(res):
    d[res[i]] = data.count(data[i])
    i += data.count(data[i])
d = sorted(d.items(), key=lambda item: item[1], reverse=True)
#print(d)
df = pd.DataFrame(d)
df.to_csv("result.csv", mode='a', index= False, encoding='utf8')
print('Done. Open result.csv')
