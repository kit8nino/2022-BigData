from bs4 import BeautifulSoup
import lxml
import time
import asyncio
import aiohttp
from fake_useragent import UserAgent


_start_time = time.time()
links = []

with open(r'Красильников Никита Дмитриевич\links.txt','r',encoding='utf-8') as file:
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
        file.write(f'{name} , {_year}')
        file.write('\n')
        print(f'обработал {count} страницу')

async def goto_page():
    tasks = []
    count = 1
    with open(r'Красильников Никита Дмитриевич\result.csv','w',encoding='utf-8') as file:
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