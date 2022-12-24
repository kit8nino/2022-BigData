import pandas as pd
from bs4 import BeautifulSoup
import requests as req
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

variant = (len("Голышкин Павел Александрович") * (datetime.date(2002, 11, 9) - datetime.date(1997, 11, 27)).days) % 5+1

top = ["Любовные романы", "Религия и духовность", "Справочная литература", "Детское", "Наука, Образование"]
top_num = [9, 15, 16, 4, 10]
alfavit = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х',
           'Ц', 'Ч', 'Ш', 'Щ', 'Э', 'Ю', 'Я']

my_top = top[variant-1]

print(variant)
print(my_top)

link = "https://royallib.com"
options = Options()
drv = webdriver.Firefox(options=options)

# находит в меню ссылку на жанр
drv.get(link)
srch = drv.find_element(by='xpath', value='//ul[@class="menu"]//li[' + str(top_num[variant-1]) + ']//a')  
link = srch.get_attribute('href')

drv.get(link)
srch = drv.find_elements(by='xpath', value='//a[starts-with(@href, "' + str(link[6:-1]) + '-ru-")]')
alph_links = [elem.get_attribute('href') for elem in srch]

books = {}
h = []
num_bukva = 0
for l in alph_links:
  
    drv.get(l)
    dvl = drv.find_elements(by='xpath', value='//a[starts-with(@href, "//royallib.com/book/")]')
    book_links = [elem.get_attribute('href') for elem in dvl]

    for s in dvl:
        books[s.get_attribute('href')] = s.get_attribute('text') # запись в словарь ссылку и текст книги

    for a in book_links:
        ye = req.get(a)
        soup = BeautifulSoup(ye.text, 'html.parser')
        # берем книгу и год
        year = ""
        try:
            for tag in soup.find_all("b"):
                if (tag.contents == ['Год издания:']):
                    year = str(tag.parent)
                    year1 = year.replace(" г.", " ")
                    ye = int(year1[year1.find('</b>') + 4:year1.find(('</td>'))])
                    h.append(ye)
                    break
            if year == "":
                h.append('No data')
        except:
            continue
    print("буква: " + alfavit[num_bukva] + " прочитана")
    num_bukva += 1
    val_books = list(books.values())
    df = pd.DataFrame()

    df['books_name'] = pd.Series(val_books)
    df['year'] = pd.Series(h)
   
    df.to_csv("biblioteca.csv", index=False, encoding='utf-8')

input('press Enter')
drv.quit()
drv.close()
