import os
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


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

books = {}
for l in author_links:
    drv.get(l)
    dwl = drv.find_elements(by='xpath', value='//a[@title="Скачать книгу"]')
    for a in dwl:
        book_name = str(a.text)
        books[book_name] = ''
        print(book_name)
        drv.get(a.get_attribute('href'))
        year = drv.find_element(by='xpath', value='/html/body/div[2]/div/div[2]/div[2]/div/table[1]/tbody/tr/td[2]/table/tbody/tr[5]/td')
        print(book_name, year.text.split()[-1])
        books[book_name] = year.text.split()[-1]

print(books)
input('press Enter')
drv.quit()
