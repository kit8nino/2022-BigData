import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import date

var=len('Руденко Сергей Денисович') * (date(2000, 12, 6) - date(1997, 11, 27)).days % 5 + 1
topics = ["lyubovnie_romani", "religiya_i_duhovnost", "spravochnaya_literatura", "detskoe", "nauka_obrazovanie"]
teme = topics[var-1]
print(var)
print(teme)
fyle = open('book.csv', 'w', newline='')
file_writer = csv.writer(fyle, delimiter=',', quotechar='"')
try:
    htps = 'https://royallib.com/genre/'+teme+'/'
    options = Options()
    options.add_experimental_option('prefs', {
        'download.default_directory': r'C:\Test',
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'safebrowsing.enabled': True
    })
    brouse = webdriver.Chrome(options=options)
    brouse.get(htps)
    silka = brouse.find_elements(by='xpath', value='//a[starts-with(@href, "//royallib.com/genre/' + teme + '-")]')
    glinks = [elem.get_attribute('href') for elem in silka]
    print(glinks)
    books = {}
    for i in glinks:
        brouse.get(i)
        silka = brouse.find_elements(by='xpath', value='//a[starts-with(@href, "//royallib.com/book/")]')
        nlinks = [elem.get_attribute('href') for elem in silka]
        print(nlinks)
        for l in nlinks:
            try:
                brouse.get(l)
                descript = brouse.find_element(by='xpath',
                                               value='/html/body/div[2]/div/div[2]/div[2]/div/table[1]/tbody/tr/td[2]/table').text.split(
                    '\n')
                year = ''
                for line in descript:
                    if line.startswith('Название:'):
                        book_name = line[10:]
                    try:
                        if line.startswith('Год издания:'):
                            year = line[13:]
                            break
                    except:
                        continue
                file_writer.writerow([f'"{book_name}", "{year}"'])

            except:
                continue
finally:
    fyle.close()
    brouse.quit()
    input('Ok or not')
