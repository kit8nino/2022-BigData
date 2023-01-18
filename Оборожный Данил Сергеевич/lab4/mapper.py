data = []

# читаем строки из файла data3.csv
for l in open(r'data3.csv', 'r', encoding="windows-1251").readlines()[1:]:
    data.append(l.split(',')[0])

# обрабатываем строки
for i in range(len(data)):
    words = data[i].split(' ')
    for j in range(len(words)):
        words[j] = words[j].replace('.','').replace('"', "").replace("?", "").replace(")", "").replace("(", "").replace(":", "").replace("!", "").replace("»", "").replace("«", "").lower()
    data[i] = words

# сортируем строки
data.sort()

# подсчитываем количество вхождений каждой строки
d = {'Предлоги/союзы': 0}
for words in data:
    for word in words:
        if len(word) <= 3:
            d['Предлоги/союзы'] += 1
            continue
        if word in d:
            d[word] += 1
        else:
            d[word] = 1

# сортируем словарь по количеству вхождений
d = sorted(d.items(), key=lambda item: item[1], reverse=True)

# записываем результаты в файл result.csv
with open("result.csv", "w", encoding='windows-1251') as result:
    result.write(f"Word,Count\n")
    for key, value in d:
        result.write(f"{key},{value}\n")
print('Check res.csv')