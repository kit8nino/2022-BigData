from functools import reduce
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt

data_ = []
m = []

mapped = open('mapped.csv', 'w', encoding='utf-8')

for l in open(r'..\lab_3\books.csv', 'r', encoding="utf8").readlines()[1:]:
    data_.append(l.split(',')[0])
    for w in data_:
        words = w.split(' ')
        for u in words:
            #  m.append(u)
            mapped.write(u + ', 1\n')

mapped.close()
res = []
res = m
#print(m)

data = list(map(lambda x: (x, 1), res))
data.sort()
#print(data)

i = 0
d = {}
while i < len(res):
    d[res[i]] = data.count(data[i])
    i += data.count(data[i])
d = sorted(d.items(), key=lambda item: item[1], reverse=True)
#print(d)
df = pd.DataFrame(d)
df.to_csv("res.csv", mode='a', index= False, encoding='utf-8')
