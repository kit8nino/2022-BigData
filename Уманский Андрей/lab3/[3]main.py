import requests
import csv
import time
from bs4 import BeautifulSoup

hyperlink = "https://royallib.com/genres.html"
section = "Детское"
book_names = []
years = []
book_years=[]
now_on=[]
list_now_on=['0-9','А','Б','В','Г','Д','Е','Ё','Ж','З','И','Й','К','Л','М','Н','О','П','Р','С','Т','У','Ф','Х','Ц','Ч','Ш','Щ','Ы','Э','Ю','Я','Eng']
i=0
j=0

#Поиск раздела
Req = requests.get(hyperlink)
BS = BeautifulSoup(Req.text, 'lxml')
hyperlink_2 = "https:" + BS.find(text=section).parent['href']
Req = requests.get(hyperlink_2)
BS = BeautifulSoup(Req.text, 'lxml')

links = []
for link in BS.find(class_="well").find_all("a"):
    links.append(link.get('href'))
print(links)



for lnk in links:
    #Обработка ссылки для вывода текущей буквы
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
            print("Обрабатываю:"+str(list_now_on[0]))
        else:
            print("Обрабатываю:"+str(list_now_on[int(now_on[0])+1]))
    except Exception:
        print('out of range')
    i+=1    
    #Работа со ссылкой
    try:
        sitefromlink = requests.get("https:"+lnk)
    except requests.exceptions.ConnectionTimeout:
        print("error!!! but i will go dalshe")
        time.sleep(5)
    content = BeautifulSoup(sitefromlink.text, 'lxml') 
    books = list(filter(lambda lunk: "book" in lunk.get("href"), content.find(class_="content").find_all("a")))
    years.clear()
    book_names.clear()
    book_years.clear()
    for b_link in books:
        years.append(b_link['href'])
        book_names.append(str(b_link.contents))
    

    #Поиск года книги
    for ind_link in range(len(years)):
        try:
            requ = requests.get("https:" + years[ind_link])
        except requests.ConnectionError:
            print("error! but i will go dal'she")
            time.sleep(3)
        soup = BeautifulSoup(requ.text, 'lxml')
        year = ""
        for tag in soup.find_all("b"):
            if (tag.contents == ['Год издания:']):
                year = str(tag.parent)
                book_years.append(int(year[year.find('</b>') + 4:year.find(('</td>'))]))
        if year == "":
            book_years.append('No data')
            

    File = open('C:/Users/User/Desktop/веб и другое/bigD/lab_3v3/data3_v10.csv', 'a')

    with File:
        writer = csv.writer(File, lineterminator="\r")
        for item in range(len(book_names)):
            writer.writerow([str(book_names[item])[2:5]+str(book_names[item])[5:len(str(book_names[item]))-2]])
    print("ok")
