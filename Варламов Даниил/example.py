from bs4 import BeautifulSoup
import requests
import lxml
import time

# headers = {
#     "accept": "*/*",
#     "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36" 
# }

# link = "https://royallib.com/book/stikalin_sergey/sovetskaya_satiricheskaya_pechat_1917_1963.html"

# req = requests.get(link,headers=headers)

# soup = BeautifulSoup(req.text,'lxml')

# table = soup.find('table')

# target = table.find_all('td')

with open(r'Варламов Даниил\page.txt','r',encoding='utf-8') as file:
    soup = BeautifulSoup(file.read(),'lxml')


target = soup.find_all('td')

items = []

for item in target:
    if 'Год' in item.text:
        s = item.text
        items.append(item.text)


print(items)
# with open(r'Варламов Даниил\page.txt','w',encoding='utf-8',newline='') as file:
#     for item in target:
#         i = str(item)
#         file.write(i)

# with open(r'Варламов Даниил\page.txt','r',encoding='utf-8') as file:
#     for line in file:
#         if 'Год' in line:
#             print(line.strip())
            