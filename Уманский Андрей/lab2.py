import csv

# Берем данные
data = []
for item in open("flavors_of_cacao.csv").readlines()[1:]:
    data.append(item.split(',')[5])
for item in open("flavors_of_cacao_2.csv").readlines()[1:]:
    data.append(item.split(',')[5])
i=0
delited=0
data.sort()
# Исключаем страны с цифрами т.к. таких не существует (очистка)
while i < len(data):
    j=0
    while j < len(str(data[i])):
        a = str(data[i])[j]
        if '0' <= a <= '9':
            delited+=1
            data.pop(i)
            i-=1
            break 
        j+=1
    i += 1
print("Удалено "+str(delited)+" записей")
# Обрабатываем данные
d = {}
i = 0
data=list(map(lambda x: ""+x+",1",data))
while i < len(data):
    d[data[i]] = data.count(data[i])
    i += data.count(data[i])
i=1
while i < (len(d)*2-1):
    print(str(d).split(',')[i-1:i+1])
    i+=2
print("ok")


