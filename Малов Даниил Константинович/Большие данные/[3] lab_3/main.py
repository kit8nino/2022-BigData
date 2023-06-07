import requests
import xlsxwriter
from time import sleep
from bs4 import BeautifulSoup

url = "https://royallib.com"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

#Выбор нужного жанра
genre = "Религия и духовность"
url_genre = ""
data = soup.find("ul", class_="menu").find_all("a")
for i in data:
    if i.text == genre:
        url_genre = "https:" + i.get("href")

#Получение информации со странички нужного жанра
response = requests.get(url_genre)
soup = BeautifulSoup(response.text, 'lxml')

#Получние ссылок страниц(А-Я)
def url_stranic():
    list_stranic = list(filter(lambda genre: "genre" in genre.get("href"), soup.find(class_="well").find_all("a")))
    for stranica in list_stranic:
        url_stranica = "https:" + stranica.get("href")
        yield url_stranica

#Получение списка книг с каждой страницы
list_books =[]
for url_stranica in url_stranic():
    response = requests.get(url_stranica)
    soup = BeautifulSoup(response.text, 'lxml')
    sleep(2)
    list_books += list(filter(lambda book: "book" in book.get("href"), soup.find(class_="content").find_all("a")))

#Получение года каждой книги
def data_books():
    for data_book in list_books:
        sleep(2)
        url_book = "https:" + data_book.get("href")
        response = requests.get(url_book)
        soup = BeautifulSoup(response.text, 'lxml')
        year = ""
        for b in soup.find_all("b"):
            if b.text == "Год издания:":
                year = str(b.parent)
                year = year[year.find('</b>') + 4:year.find(('</td>'))]
        if year == "":
            year = "Дата отсутствует"
        book = data_book.text
        print(book)
        yield book, year

#Запись в Excel документ
def writer(parametrs):
    book = xlsxwriter.Workbook(r"C:\Users\Владимир\Documents\Study\3 курс\5 семестр\Большие данные\lab_3\books.xlsx")
    page = book.add_worksheet("Книги")

    row = 0
    column = 0

    page.set_column("A:A", 115)
    page.set_column("B:B", 15)

    for item in parametrs():
        page.write(row, column, item[0])
        page.write(row, column+1, item[1])
        row = row + 1

    book.close()

writer(data_books)