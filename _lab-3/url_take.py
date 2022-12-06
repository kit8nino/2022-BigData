import os
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import threading


link = "https://royallib.com"
options = Options()
options.add_experimental_option("prefs", {
  "download.default_directory": r"D:\Test",
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
})

drv = webdriver.Chrome(options=options)

drv.get(link)

srch = drv.find_element(by='id', value="q")
author = "Терри Пратчетт" # input("Author: ")
srch.send_keys(author + Keys.RETURN)

srch = drv.find_elements(by='xpath', value='//a[starts-with(@href, "//royallib.com/author/")]')
author_links = [elem.get_attribute('href') for elem in srch]

def get_year(link, a, f):
    d = webdriver.Chrome()
    d.get(link)
    year = d.find_element(by='xpath', value='/html/body/div[2]/div/div[2]/div[2]/div/table[1]/tbody/tr/td[2]/table/tbody/tr[5]/td')
    f.write(a + ',' + year.text.split()[-1]+'\n')
    d.quit()


books = {}
for l in author_links:
    drv.get(l)
    dwl = drv.find_elements(by='xpath', value='//a[@title="Скачать книгу"]')
    book_names = list(map(lambda x: x.text, dwl))
    for b in book_names:
        books[b] = ''
    with open('terry.csv', 'w', encoding='utf-8-sig') as file:
        t = []
        for a in dwl:
            t.append(threading.Thread(target=get_year, args=(a.get_attribute('href'), a.text, file)))

        for i in t:
            i.run()
        # books[book_name] = ''
            # drv.get(a.get_attribute('href'))
            # year = drv.find_element(by='xpath', value='/html/body/div[2]/div/div[2]/div[2]/div/table[1]/tbody/tr/td[2]/table/tbody/tr[5]/td')

print(books)
input('press Enter')
drv.quit()
