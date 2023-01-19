import requests
import csv
from bs4 import BeautifulSoup
counter = 0
href_novels = []
book_years = []
name_novels =[]
years = []  
url = 'https://royallib.com/genre/lyubovnie_romani/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

for link in soup.find(class_='well').find_all('a'):
    href_novels.append(link['href'])  
   
for link_novels in href_novels:
    try:
        links_ns = requests.get('https:' + link_novels)
    except:
        continue
    content = BeautifulSoup(links_ns.text,'lxml')
    books = list(filter(lambda x: 'book' in x.get('href'),content.find(class_='content').find_all('a')))

    for link in books:
        years.append(link['href'])
        name_novels.append(link.contents)
    
    for l_books in range(len(years)):
        try:
            n_resp=requests.get('https:' + years[l_books])
        except:
            continue
        n_content = BeautifulSoup(n_resp.text,'lxml')
        year = ""
        for tag in n_content.find_all('b'):
            if (tag.contents == ['Год издания:']):
                year = str(tag.parent)
                book_years.append(int(year[year.find('</b>') + 4:year.find(('</td>'))])) 
        if(year == ""):
            book_years.append("no data")
        counter+=1  
        print("процесс пошел",counter)

    File = open('report.csv', 'w')
    with File:
        writer = csv.writer(File)
        for item in range(len(name_novels)):
            writer.writerow([", ".join(map(str,name_novels[item])), book_years[item]])
        
    
     