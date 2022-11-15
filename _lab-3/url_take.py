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
        books[a.get_attribute('text')] = a.get_attribute('href')

print(books)
input('press Enter')
drv.quit()
