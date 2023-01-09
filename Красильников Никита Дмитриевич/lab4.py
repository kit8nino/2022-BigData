import re
from collections import Counter

data = []

with open(r'Красильников Никита Дмитриевич\result.csv','r',encoding='utf-8') as file:
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

from collections import Counter
from matplotlib import pyplot as plt
with open(r'Красильников Никита Дмитриевич\splitted.txt','w',encoding='utf-8') as file:
     file.write(str(res1))
number = 1
ignore = []
for i in range(2500):
    number = number + 1
    ignore.append(str(number))
print(ignore)
counter = Counter(res1)
for word in list(counter):
    if word in ignore or len(word)<3:
            del counter[word]
print(counter.most_common(5))

spisok=[]
counter = counter.most_common(15)
for i in res1:
    if len(i)==4:
        continue
    else:
        spisok.append(i)
print(spisok)
labels, values = zip(*counter)
colors = ['blue' if (bar == max(values)) else 'grey' for bar in values]
plt.bar(labels, values, color=colors)
plt.xlabel('Слово')
plt.ylabel('Количество')
plt.grid(color = 'red', alpha = 0.3, linestyle = '-', linewidth = 0.5)
plt.show()
