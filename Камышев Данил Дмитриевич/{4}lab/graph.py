import csv
import matplotlib as mpl
import matplotlib.pyplot as plt
import functools


def myCheck(line):
    try:
        if int(line) >= 2000:
            return True
    except ValueError:
        return False


names = []
years = []

with open('romantic.csv', newline='') as File:
    reader = csv.reader(File, dialect='excel')
    for row in reader:
        if len(row) != 0:
            years.append(row[1])
            names.append(str(row[0]).strip("'[]"))
data = dict(zip(names, years)) # данные из файла
words = [] # список слов
for name in data.keys():
     words.extend(name.split())
# Процент книг вышедших после 2000
a = list(filter(myCheck, data.values()))
b = []
for i in data.values():
    if not (i in a):
        b.append(i)
A = [len(a), len(b)]
B = ['после и в 2000', 'до 2000']
plt.title('Книги выпущенные')
plt.pie(A, autopct='%0.1f', radius=1, labels=B)
plt.show()
ask = input('Хотите увидеть ещё диаграммы? (Введите что-угодно для подтверждения)')
if (ask):
    # Какие слова повторяются чаще всего
    words2 = sorted(set(words))  # список отсортированных слов без повторов
    myDict = {x: words.count(x) for x in words2}  # словарь в котором ключ - слово, значение - кол-во повторов
    sortedDict = {}  # словарь по значениям в обратном порядке
    sortedKeys = sorted(myDict, key= myDict.get,reverse=True)
    for w in sortedKeys:
        sortedDict[w] = myDict[w]
    # сделаю топ 20
        mpl.rcParams.update({'font.size': 7})
        plt.title("Топ 20 слов в любовных романах")
        list1 = list(sortedDict.keys())[0:20]
        list1.append('Другое')
        list2 = list(sortedDict.values())[0:20]
        list2.append(sum(list(sortedDict.values())[20:]))
        DICT = dict(zip(list1, list2))
        print(DICT)
        plt.pie(DICT.values(),autopct='%0.1f', radius = 1, explode= [0.15] + [0 for _ in range(len(DICT.keys())-1)] )
        plt.legend(bbox_to_anchor= (-0.3, 0, 0.25, 0.25), loc = 'lower left', labels = DICT.keys())
        plt.draw()
        plt.pause(3.5)
        plt.close()