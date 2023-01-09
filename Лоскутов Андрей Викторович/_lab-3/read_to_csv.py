from selenium import webdriver
from bs4 import BeautifulSoup
import asyncio
import aiohttp
from fake_useragent import UserAgent
import lxml

links = []

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
        file.write(f'{name} , {_year}')
        file.write('\n')
        print(f'обработал {count} страницу')

async def goto_page():
    tasks = []
    count = 1
    with open(r'Лоскутов Андрей Викторович\result.csv','w',encoding='utf-8') as file:
        async with aiohttp.ClientSession() as session:
            for link in links:
                count = count+1
                task = asyncio.create_task(get_year(session=session,link=link,count=count,file=file))
                tasks.append(task)
            await asyncio.gather(*tasks)

def main():
    print('Вариант 3 тема Справочная литература')

    link = 'https://royallib.com/genre/spravochnaya_literatura/'
    drv = webdriver.Chrome()
    drv.get(link)
    srch = drv.find_elements(by='xpath', value='//a[starts-with(@href, "//royallib.com/genre/spravochnaya_literatura-")]')
    genre_links = [elem.get_attribute('href') for elem in srch]
    for i in genre_links:
        drv.get(i)
        srch = drv.find_elements(by='xpath', value='//a[starts-with(@href, "//royallib.com/book/")]')
        name_links = [elem.get_attribute('href') for elem in srch]
        for l in name_links:
            links.append(l)
    drv.quit()

    asyncio.run(goto_page())

if __name__=='__main__':
    main()
