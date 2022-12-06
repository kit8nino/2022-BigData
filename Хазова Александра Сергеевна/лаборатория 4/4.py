from functools import reduce
import numpy as np
import pandas as pd
import itertools
#import matplotlib.pyplot as plt

data_ = []
m = []

mapped = open('mapped.csv', 'w', encoding='utf-8')

for l in open(r'C:\Users\Сергей\Documents\parsing\books.csv', 'r', encoding="utf8").readlines()[1:]:
    data_.append(l.split(',')[0])
#data = itertools.islice(data_, 100) 
for w in data_:
    words = w.split(' ')
    for u in words:
        #m.append(u)
        mapped.write(u + '\n')

mapped.close()

res = [] 
for r in open(r'C:\Users\Сергей\Documents\parsing\mapped.csv', 'r', encoding='utf-8').readlines():
    res.append(r.split('\n')[0])

res = tuple(res)


data = list(map(lambda x: (x, 1), res))
data.sort()
print(res)

i = 0
d = {}

while i < len(res):
    d[res[i]] = data.count(data[i])
    i += data.count(data[i])
d = sorted(d.items(), key=lambda item: item[1], reverse=True)
#print(d)
df = pd.DataFrame(d)
df.to_csv("res.csv", mode='a', index= False, encoding='utf-8')
print('Check res.csv')
