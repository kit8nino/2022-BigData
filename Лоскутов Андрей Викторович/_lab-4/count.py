import re
from collections import Counter

data = []
with open(r'Лоскутов Андрей Викторович\result.csv','r',encoding='utf-8') as file:
    data = file.readlines()
for i in range(len(data)):
    data[i] = re.split('\W',data[i])
_data = []
for i in data:
    for item in i:
        _data.append(item)
_data = [e for e in _data if e]
res = dict(Counter(_data))
res1 = {k: v for k, v in sorted(res.items(), key=lambda item: item[1],reverse=True)}
with open(r'Лоскутов Андрей Викторович\final.txt','w',encoding='utf-8') as file:
    file.write(str(res1))