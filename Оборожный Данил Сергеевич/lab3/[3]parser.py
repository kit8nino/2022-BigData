import requests
import csv
import time
from random import randint
from bs4 import BeautifulSoup

hyperlink = "https://royallib.com/genres.html"
section = "Любовные романы"
years = []
list_now_on=['0-9','А','Б','В','Г','Д','Е','Ё','Ж','З','И','Й','К','Л','М','Н','О','П','Р','С','Т','У','Ф','Х','Ц','Ч','Ш','Щ','Ы','Э','Ю','Я','Eng']
tier1=['Аромат', 'Пучеглазие', 'Слабоумие', 'Напоминание', 'Дибилизм', 'Обваривание', 'Икрометание', 'Именование', 'Жопа', 'Анархизм', 'Центризм', 'Капитализм', 'Коммунизм', 'Аристократизм', 'Питонизм']
tier2=['Навоза', 'Утконоса', 'Сковороды', 'Лепёшки', 'Термостата', 'Гиганта мысли', 'Носка', 'Прокурора', 'Токседермиста', 'Таксиста', 'Букета', 'Бомжа', 'Шаурмы', 'Чебуреков', 'Благовоний']
#33
i=0
#Поиск раздела
Req = requests.get(hyperlink)
BS = BeautifulSoup(Req.text, 'lxml')
hyperlink_2 = "https:" + BS.find(text=section).parent['href']
Req = requests.get(hyperlink_2)
BS = BeautifulSoup(Req.text, 'lxml')

links = []
for link in BS.find(class_="well").find_all("a"):
    links.append(link.get('href'))
#print(links)



for link in links:
    try:
        print("Обрабатываю:" + list_now_on[i] + " " + tier1[randint(0, len(tier1)-1)] + " " + tier2[randint(0, len(tier2)-1)])
    except Exception:
        print('out of range')
    i+=1    

    try:
        sitefromlink = requests.get("https:"+link)
    except requests.exceptions.ConnectionTimeout:
        print("ConnectionTimeout")

    content = BeautifulSoup(sitefromlink.text, 'lxml') 
    books = list(filter(lambda lunk: "book" in lunk.get("href"), content.find(class_="content").find_all("a")))

    File = open('C:/Users/Den-O/Desktop/data3.csv', 'a')
    writer = csv.writer(File, lineterminator="\r")

    for b_link in books:

        book_name = str(b_link.contents)[2:-2]

        try:
            request = requests.get("https:" + b_link['href'])
        except requests.ConnectionError:
            print("ConnectionError")

        dataParse = BeautifulSoup(request.text, 'lxml')
        year = "No data"

        for tag in dataParse.find_all("b"):
            if (tag.contents == ['Год издания:']):
                year = str(tag.parent)
                year = int(year[year.find('</b>') + 4:year.find(('</td>'))])
        writer.writerow([book_name, str(year)])


    print("ok")