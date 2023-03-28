import requests
import csv
import string
import math
import statistics as stat
from functools import reduce
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

data=[]
year_of_izdania=[]
years_dict={"ранее":0,"1900е":0,"1910е":0,"1920е":0,"1930е":0,"40е":0,"50е":0,"60е":0,"70е":0,"80е":0,"90е":0,"00е":0,"10е":0,"позднее":0,}
#mapping (+filter)
for item in open("data3_v10.csv").readlines()[1:]:
    item = item.replace('-', ' ')
    #Убираем пунктуацию
    for p in string.punctuation:
        if p in item:
            item = item.replace(p, '')
    #Удаляем год издания и переводим в нижний регистр
    item = item.replace('No data', '1234')
    if item[len(item)-5:len(item)-1]!="1234" and item[len(item)-5:len(item)-1]!=" 123":
        year_of_izdania.append(item[len(item)-5:len(item)-1])
    item = item[0:len(item)-5].lower()    
    #Делим на слова
    for word in item.split(" "):
        data.append(word)
#reducing
d=dict((x, data.count(x)) for x in set(data) if data.count(x) > 31) # 31 оптимально для графика
del(d[""])
try:
    for year in year_of_izdania:
        if int(year)<1900:
            years_dict["ранее"]+=1
        elif int(year)<1910:
            years_dict["1900е"]+=1
        elif int(year)<1920:
            years_dict["1910е"]+=1
        elif int(year)<1930:
            years_dict["1920е"]+=1
        elif int(year)<1940:
            years_dict["1930е"]+=1
        elif int(year)<1950:
            years_dict["40е"]+=1
        elif int(year)<1960:
            years_dict["50е"]+=1
        elif int(year)<1970:
            years_dict["60е"]+=1
        elif int(year)<1980:
            years_dict["70е"]+=1
        elif int(year)<1990:
            years_dict["80е"]+=1
        elif int(year)<2000:
            years_dict["90е"]+=1
        elif int(year)<2010:
            years_dict["00е"]+=1
        elif int(year)<2020:
            years_dict["10е"]+=1
        else:
            years_dict["позднее"]+=1
except:
    print("исключен год:",year)
#sorting
d=dict(sorted(d.items(), key=lambda item: item[1]))
#Рисуем график
plt.pie(d.values(),labels=d.keys())
plt.axis('equal')
plt.suptitle('Самые частовстречающиеся слова')
plt.show()
#Рисуем график годов выхода книг
plt.bar(years_dict.keys(),years_dict.values())
plt.title("Распределение книг по годам")
plt.grid(True)
plt.show()
#Вычисляем значимые (и не очень) статистические параметры
full_values=list((data.count(x)) for x in set(data) if data.count(x) > 0)
full_values.sort()
median=(full_values[int(len(full_values)/2)]+full_values[int(len(full_values)/2)+1])/2 if (len(full_values)%2==0) else full_values[int(len(full_values)/2)+1]
moda=dict((x, full_values.count(x)) for x in set(full_values))
moda=dict(sorted(moda.items(), key=lambda item: item[1]))
for key in moda.keys():
    moda_result=key
CKO_help_list=list((full_values[x]-np.average(full_values))**2 for x in full_values) 
CKO=math.sqrt((sum(CKO_help_list))/len(full_values))

mat_ozidanie_list=[]
for key in moda:
    mat_ozidanie_list.append(int(key)*moda[key]/len(full_values))
print("Статистика по частоте слов")
print("Среднее:",np.average(full_values))
print("Медианное:",median)
print("Максимальное:",max(full_values))
print("Минимальное:",min(full_values))
print("Размах:",max(full_values)-min(full_values))
print("Мода:", moda_result)
print("Стандартное отклонение:",np.std(full_values))
print("СКО:",CKO)
print("Дисперсия:",CKO**2)
print("Мат ожидание:",sum(mat_ozidanie_list))
print(f"Коэффициент вариации: "+str(CKO/np.average(full_values)*100)+"%")
