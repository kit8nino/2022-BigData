import pandas as pd
from bs4 import BeautifulSoup 
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

variant = (len("Хазова Александра Сергеевна") * (datetime.date(2002,8,5)-datetime.date(1997,11,27)).days)%5
topics = ["Любовные романы", "Религия и духовность", "Справочная литература", "Детское", "Наука, Образование"]
my_topic = topics[variant]
variant+=1
print(variant)
print(my_topic)

link = "https://royallib.com"
options = Options()
drv = webdriver.Chrome(options=options)

drv.get(link)
srch = drv.find_element(by='xpath', value='//ul[@class="menu"]//li['+str(2*variant)+']//a') #"https://royallib.com/genre/nauka_obrazovanie/" 
link = srch.get_attribute('href')

drv.get(link)
srch = drv.find_elements(by = 'xpath', value = '//a[starts-with(@href, "'+str(link[6:-1])+'-ru-")]')
alph_links = [elem.get_attribute('href') for elem in srch]

books = {}
h = {}
  
for l in alph_links:
    drv.get(l)
    dvl = drv.find_elements(by = 'xpath', value = '//a[starts-with(@href, "//royallib.com/book/")]')
    book_links = [elem.get_attribute('href') for elem in dvl]
    for s in dvl:
        books[s.get_attribute('href')] = s.get_attribute('text')

    for a in book_links:
        drv.get(a)
        srch_autor = drv.find_elements(by = 'xpath', value = '//a[starts-with(@href, "//royallib.com/author/")]')
        #srch_ye = drv.find_element(by = 'xpath', value = '/html/body/div[2]/div/div[2]/div[2]/div/table[1]/tbody/tr/td[2]/table/tbody/tr[5]/td')
        for n in srch_autor:
            h[n.get_attribute('href')] = n.get_attribute('text')

    val_h = list(h.values())        
    val_books = list(books.values())
    df = pd.DataFrame()
    df['autor'] = pd.Series(val_h)
    df['books_name'] = pd.Series(val_books)
    #pd.DataFrame({"books_name": books, "year": year})
    df.to_csv("books.csv", index= False, encoding='utf-8')

input('press Enter')
drv.quit()
drv.close()
