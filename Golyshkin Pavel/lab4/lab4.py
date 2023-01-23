import re
from collections import Counter
from matplotlib import pyplot as plt

def yearD():
    f = open('biblioteca.csv','r',encoding='cp437',errors='ignore')

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
    plt.title('Жанр "Наука, Образование": колличество книг по годам')
    plt.xlabel('Год:')
    plt.ylabel('Количество:')
    plt.grid(color = 'red', alpha = 0.2, linestyle = '-', linewidth = 0.3)
    plt.show()
    f.close()

def pieWordD():
    f = open('biblioteca.csv', 'r',encoding='utf-8',errors='ignore')
    file = re.sub('[^а-яё, ]', '', f.read().lower()).split()
    words = list(filter(lambda x: len(x) >=3, file))
    counter = Counter(words)
    counter = counter.most_common(10)
    labels, values = zip(*counter)

    plt.pie(values, labels=labels)
    plt.title('Самые популярные слова в названии:')
    plt.show()
    f.close()

pieWordD()
yearD()