from collections import Counter
import re 
from matplotlib import pyplot as grap

def bar():
    csv = open('spisok.csv', 'r')
    file = re.findall('\d{4}', csv.read())
    words = filter(lambda x: int(x) >1000, file)
    data = list(map(int, words))
    schet = Counter(data)
    schet = schet.most_common(200)
    schet =  sorted(schet, key=lambda x: x[0], reverse=True)
    print(schet)
    labels, values = zip(*schet)

    colors = ['red' if (bar == max(data)) else 'pink' for bar in values]
    grap.bar(labels, values, color=colors)
    grap.title('"Любовные романы": количество книг в год')
    grap.xlabel('Год')
    grap.ylabel('Количество')
    grap.grid(color = 'red', alpha = 0.3, linestyle = '-', linewidth = 0.5)
    grap.show()
    csv.close()

def pie():
    csv = open('spisok.csv', 'r')
    file = re.sub('[^a-zа-яё, ]', '', csv.read().lower()).split()
    words = list(filter(lambda x: len(x) >3, file))
    schet = Counter(words)
    schet = schet.most_common(10)
    labels, values = zip(*schet)
    
    grap.pie(values, labels=labels)
    grap.title('Частовстречающиеся слова')
    grap.show()
    csv.close()

bar()
pie()
