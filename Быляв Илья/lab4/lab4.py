import re
from collections import Counter
from matplotlib import pyplot as plt

def mr():
    f = open('report.csv', 'r')
    file = re.findall('\d{4}', f.read())
    words = filter(lambda x: int(x) <= 2023, file)
    data = list(map(int, words))
    counter = Counter(data)
    counter = counter.most_common()
    print(counter)
    counter =  sorted(counter, key=lambda x: x[0], reverse=True)
    labels, values = zip(*counter)

    colors = ['blue' if (bar == max(values)) else 'grey' for bar in values]

    plt.bar(labels, values, color=colors)
    plt.title('Жанр "Любовные романы": количество книг в год')
    plt.xlabel('Год:')
    plt.ylabel('Количество:')
    plt.grid(color = 'red', alpha = 0.2, linestyle = '-', linewidth = 0.3)
    plt.show()
    f.close()

def pie():
    f = open('report.csv', 'r')
    file = re.sub('[^a-zа-яё, ]', '', f.read().lower()).split()
    words = list(filter(lambda x: len(x) > 3, file))
    counter = Counter(words)
    counter = counter.most_common(15)
    labels, values = zip(*counter)

    plt.pie(values, labels=labels)
    plt.title('Самые популярные слова в названии:')
    plt.show()
    f.close()

mr()
pie()