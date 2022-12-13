import requests
import csv
import time
from bs4 import BeautifulSoup

link = "https://royallib.com/genres.html"
my_genre = "Любовные романы"
names = []
links_years = []
Ryears=[]
counter = 0
# Нахожу свой жанр
resp = requests.get(link)
soup = BeautifulSoup(resp.text, 'lxml')
new_link = "https:" + soup.find(text=my_genre).parent['href']
resp = requests.get(new_link)
soup = BeautifulSoup(resp.text, 'lxml')

# все ссылки по теме по алфавиту
LIST_OF_LINKS = []
for link in soup.find(class_="well").find_all("a"):
    LIST_OF_LINKS.append(link.get('href'))
print(LIST_OF_LINKS)
for linkus in LIST_OF_LINKS:
    # достаем список книг
    try:
        sitefromlink = requests.get("https:"+linkus)
    except requests.exceptions.ConnectionTimeout:
        print("Connection refused by the server..")
        print("Let me sleep for 5 seconds")
        print("ZZzzzz...")
        time.sleep(5)
        print("Was a nice sleep, now let me continue...")
    content = BeautifulSoup(sitefromlink.text, 'lxml') # print(content)
    books = list(
        filter(lambda lunk: "book" in lunk.get("href"), content.find(class_="content").find_all("a"))
    )

    # достаем названия книг и ссылки на книги из тэга
    for b_link in books:
        links_years.append(b_link['href'])
        names.append(str(b_link.contents))
    #print(links_years)

    # достаем год издания со страницы книги, если года нет "No data"
    for ind_link in range(len(links_years)):
        #print(ind_link,  names[ind_link])
        try:
            requ = requests.get("https:" + links_years[ind_link])
        except requests.exceptions.ConnectionTimeout:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
        soup = BeautifulSoup(requ.text, 'lxml')
        year = ""
        for tag in soup.find_all("b"):
            if (tag.contents == ['Год издания:']):
                year = str(tag.parent)
                Ryears.append(int(year[year.find('</b>') + 4:year.find(('</td>'))]))
        if year == "":
            Ryears.append('No data')
        #counter+=1
        #print("Взлом казино, выкачано:",counter, "т.р.")

    File = open('Romantic.csv', 'w')

    with File:
        writer = csv.writer(File)
        for item in range(len(names)):
            writer.writerow([names[item], Ryears[item]])
