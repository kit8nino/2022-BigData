import re
from collections import Counter
from matplotlib import pyplot as plt

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

with open(r'Лоскутов Андрей Викторович\final.txt','w', encoding='utf-8') as file:
    file.write(str(res1))

def mr():
    f = open(r'Лоскутов Андрей Викторович\final.txt', 'r', encoding='utf-8')
    file = re.findall('\d{4}', f.read())
    words = filter(lambda x: int(x) > 1000, file)
    data = list(map(int, words))
    counter = Counter(data)
    counter = counter.most_common()
    counter =  sorted(counter, key=lambda x: x[0], reverse=True
    )
    labels, values = zip(*counter)

    colors = ['blue' if (bar == max(values)) else 'grey' for bar in values]

    plt.bar(labels, values, color=colors)
    plt.title('Жанр "Справочная литература": количество книг в год')
    plt.xlabel('Год:')
    plt.ylabel('Количество:')
    plt.grid(color = 'red', alpha = 0.2, linestyle = '-', linewidth = 0.3)
    plt.show()
    f.close()

def pie():
    f = open(r'Лоскутов Андрей Викторович\final.txt', 'r', encoding='utf-8')
    file = re.sub('[^a-zа-яё, ]', '', f.read().lower()).split()
    words = list(filter(lambda x: len(x) >3, file))
    counter = Counter(words)
    counter = counter.most_common(15)
    labels, values = zip(*counter)

    plt.pie(values, labels=labels)
    plt.title('Самые популярные слова в названии:')
    plt.show()
    f.close()

mr()
pie()