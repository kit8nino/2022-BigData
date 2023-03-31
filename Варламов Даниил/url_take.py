# import os
# from selenium.webdriver.common.keys import Keys
# from selenium import webdriver
# from selenium.webdriver.edge.options import Options
# import threading

# link = "https://royallib.com/genre/spravochnaya_literatura-ru-6.html"
# link = "https://royallib.com"
# options = Options()
# options.add_experimental_option("prefs", {
#   "download.default_directory": r"D:\Test",
#   "download.prompt_for_download": False,
#   "download.directory_upgrade": True,
#   "safebrowsing.enabled": True
# })

# drv = webdriver.Edge()

# drv.get(link)

# srch = drv.find_element(by='id', value="q")
# author = "Терри Пратчетт" # input("Author: ")
# srch.send_keys(author + Keys.RETURN)

# srch = drv.find_elements(by='xpath', value='//a[starts-with(@href, "//royallib.com/book/")]')
# links = [elem.get_attribute('href') for elem in srch]


# def get_year(link, a):
#     d = webdriver.Edge()
#     d.get(link)
#     year = d.find_element(by='xpath', value='/html/body/div[2]/div/div[2]/div[2]/div/table[1]/tbody/tr/td[2]/table/tbody/tr[5]/td')
#     print(year.text)# f.write(a + ',' + year.text.split()[-1]+'\n')
#     d.quit()


# books = {}
# for l in author_links:
#     drv.get(l)
#     dwl = drv.find_elements(by='xpath', value='//a[@title="Скачать книгу"]')
#     book_names = list(map(lambda x: x.text, dwl))
#     for b in book_names:
#         books[b] = ''
#     #with open('terry.csv', 'w', encoding='utf-8-sig') as file:
#     t = []
#     for a in dwl:
#         t.append(threading.Thread(target=get_year, args=(a.get_attribute('href'), a.text)))

#         # for i in t:
#         #     i.run()
#         # books[book_name] = ''
#             # drv.get(a.get_attribute('href'))
#             # year = drv.find_element(by='xpath', value='/html/body/div[2]/div/div[2]/div[2]/div/table[1]/tbody/tr/td[2]/table/tbody/tr[5]/td')
# print(t)
# # print(books)
# input('press Enter')
# drv.quit()
#-------------------------------------
# from multiprocessing import Pool
# def f(x):
#     return x*x

# if __name__ == '__main__':
#     with Pool (5) as p:
#         print(p.map(f, [1,2,3  ]))
#------------------------------------
from bs4 import BeautifulSoup
import lxml
import time
import asyncio
import aiohttp
from fake_useragent import UserAgent


_start_time = time.time()
links = []

with open(r'Варламов Даниил\links.txt','r',encoding='utf-8') as file:
    links = file.readlines()
    links = [item.strip() for item in links]

async def get_year(session,link,count,file):
    headers = {
        'user-agent': UserAgent().random
    }
    async with session.get(url=link,headers=headers) as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, 'lxml')
        try:
            table = soup.find('table')
            target = table.find_all('td')
        except Exception as ex:
            print(ex)
            file.write(link)
            file.write('\n')
            return
        items = []
        for item in target:
            items.append(item.text)
        items = [item.strip() for item in items if str(item)]
        items = [item.split('\n') for item in items]
        items = [item for item in items if item]
        items.pop(1)
        name = ''
        _year = ''
        for item in items:
            for i in item:
                if 'Название' in i:
                    n = item[2].strip()
                    name = n
                if 'Год издания' in i: 
                    n = item[2].strip()
                    _year = n
        file.write(f'{name},{_year}')
        file.write('\n')
        print(f'обработал {count} страницу')

async def goto_page():
    tasks = []
    count = 1
    with open(r'Варламов Даниил\result.csv','w',encoding='utf-8') as file:
        async with aiohttp.ClientSession() as session:
            for link in links:
                count = count+1
                task = asyncio.create_task(get_year(session=session,link=link,count=count,file=file))
                tasks.append(task)
            await asyncio.gather(*tasks)
        
def main():
    asyncio.run(goto_page())

if __name__=='__main__':
    main()




_finish_time_ = time.time()

_work_time_ = _finish_time_ - _start_time

print('Конец')
print(f'Время работы программы: {_work_time_}')



#     req = requests.get(link,headers=headers)
#     pages.append(req.text)
#     # try:
#     soup = BeautifulSoup(req.text,"lxml")
#     table = soup.find('table')
#     tbody = table.find('tbody')
#     row = tbody.find_all('tr')
#     for r in row:
#         reqtable = row.find('table')
#         reqtbody = reqtable.find('tbody')
#         rows = reqtbody.find_all('tr')
#         for item in rows:
#             td = row.find('td')
#             print(td.text)
#             time.sleep(2)
#     # except Exception as ex:
#     #     print(ex)


#     count = count+1
#     print(f"Сделано: {count}")

# print(pages)