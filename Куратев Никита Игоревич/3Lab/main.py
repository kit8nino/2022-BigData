import requests
import csv
import time
from bs4 import BeautifulSoup

hyperlink = "https://royallib.com/genres.html"
temi = ["Любовные романы","Религия и духовность","Справочная литература","Детское","Наука, Образование"]
Imya_knig = []
Goda = []
God_knigi=[]
now_on=[]
lists=['0-9','А','Б','В','Г','Д','Е','Ё','Ж','З','И','Й','К','Л','М','Н','О','П','Р','С','Т','У','Ф','Х','Ц','Ч','Ш','Щ','Ы','Э','Ю','Я','Eng']
i=0
j=0
h = 19%5+1 #(19.10.2001)->19%5+1 \Как я понял\
Vibor = temi[h-1]

Req = requests.get(hyperlink)
BS = BeautifulSoup(Req.text, 'html.parser') # lxml ne rabotaet
hyperlink_2 = "https:" + BS.find(text=Vibor).parent['href']
Req = requests.get(hyperlink_2)
BS = BeautifulSoup(Req.text, 'html.parser')

links = []
for link in BS.find(class_="well").find_all("a"):
    links.append(link.get('href'))
print(links)

print("Тема - ",Vibor)

File = open('Result.csv', 'a',encoding='utf-8') 
with File:
    writer = csv.writer(File, lineterminator="\r")
    writer.writerow(['Название книги', 'Год'])
File.close()
for lnk in links:
    now_on.clear()
    j=0
    while j < len(str(lnk)):
        s_int = ''
        a = str(lnk)[j]
        while '0' <= a <= '9':
            s_int += a
            j += 1
            if j < len(str(lnk)):
                a = str(lnk)[j]
            else:
                break
        j += 1
        if s_int != '':
            now_on.append(int(s_int))
    try:
        if i==0:
            print("Обрабатка:"+str(lists[0]))
        else:
            print("Обрабатка:"+str(lists[int(now_on[0])+1]))
    except Exception:
        print('out of range')
    i+=1    

    try:
        sitefromlink = requests.get("https:"+lnk)
    except requests.exceptions.ConnectionTimeout:
        print("error")
        time.sleep(5)
    content = BeautifulSoup(sitefromlink.text, 'html.parser') 
    books = list(filter(lambda lunk: "book" in lunk.get("href"), content.find(class_="content").find_all("a")))
    Goda.clear()
    Imya_knig.clear()
    God_knigi.clear()
    for b_link in books:
        Goda.append(b_link['href'])
        Imya_knig.append(str(b_link.contents))
    

    for ind_link in range(len(Goda)):
        try:
            requ = requests.get("https:" + Goda[ind_link])
        except requests.ConnectionError:
            print("error")
            time.sleep(3)
        soup = BeautifulSoup(requ.text, 'html.parser')
        year = ""
        for tag in soup.find_all("b"):
            if (tag.contents == ['Год издания:']):
                year = str(tag.parent)
                for s in year.split(): 
                    if s.isdigit():
                        God_knigi.append(s)
        if year == "":
            God_knigi.append('Нет данных')
            

    File = open('Result.csv', 'a',encoding='utf-8') 

    with File:
        writer = csv.writer(File, lineterminator="\r")
        for item in range(len(Imya_knig)):
            writer.writerow([str(Imya_knig[item])[2:5]+str(Imya_knig[item])[5:len(str(Imya_knig[item]))-2] , God_knigi[item]])
    print("Done")
