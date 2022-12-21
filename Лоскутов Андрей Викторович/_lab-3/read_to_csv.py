from threading import Thread
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

result1 = []
result2 = []

def write(links, result):
    options = Options()
    options.add_experimental_option('prefs', {
        'safebrowsing.enabled': True
    })
    drv = webdriver.Chrome(options=options)
    for l in links:
        drv.get(l)
        dvl = drv.find_elements(by = 'xpath', value = '//a[starts-with(@href, "//royallib.com/book/")]')
        book_links = [elem.get_attribute('href') for elem in dvl]
        for a in book_links:
            drv.get(a)
            try:
                description = drv.find_element(by='xpath', value='/html/body/div[2]/div/div[2]/div[2]/div/table[1]/tbody/tr/td[2]/table').text.split('\n')
            except:
                continue
            finally:
                name = ''
                year = ''
                for line in description:
                    if line.startswith('Название:'):
                        name = line[10:]
                    if line.startswith('Год издания:'):
                        year = line[13:]
                        break
                if year == '':
                    year = 'none'
                print(name + ' ' + year)
                result.append({ 'Название' : name, 'Год издания' : year })
    drv.quit()
    return result

print('Вариант 3 тема Справочная литература')

link = 'https://royallib.com/genre/spravochnaya_literatura/'
options = Options()
options.add_experimental_option('prefs', {
    'safebrowsing.enabled': True
})
drv = webdriver.Chrome(options=options)

drv.get(link)
srch = drv.find_elements(by='xpath', value='//a[starts-with(@href, "//royallib.com/genre/spravochnaya_literatura-")]')
links = [elem.get_attribute('href') for elem in srch]
drv.quit()

t1 = Thread(target=write, args=(links[:len(links)//2], result1))
t1.start()
write(links[len(links)//2:], result2)
t1.join()

with open('result.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = ['Название', 'Год издания'])
    writer.writeheader()
    writer.writerows(result1)
    writer.writerows(result2)
print(result1)
print(result2)

csvfile.close()