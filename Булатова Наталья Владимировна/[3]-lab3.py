import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

f = open('result_lab3.csv', 'w', newline='')
file_writer = csv.writer(f, delimiter=',', quotechar='"')
try:
  link = 'https://royallib.com/genre/spravochnaya_literatura/'
  options = Options()
  options.add_experimental_option('prefs', {
    'download.default_directory': r'D:\Test',
    'download.prompt_for_download': False,
    'download.directory_upgrade': True,
    'safebrowsing.enabled': True
  })
  drv = webdriver.Chrome(options=options)
  drv.get(link)
  srch = drv.find_elements(by='xpath', value='//a[starts-with(@href, "//royallib.com/genre/spravochnaya_literatura-")]')
  granre_links = [elem.get_attribute('href') for elem in srch]
  print(granre_links)
  books = {}
  for i in granre_links:
      drv.get(i)
      srch = drv.find_elements(by='xpath', value='//a[starts-with(@href, "//royallib.com/book/")]')
      name_links = [elem.get_attribute('href') for elem in srch]
      print(name_links)
      for l in name_links:
        try:
          drv.get(l)
          descript = drv.find_element(by='xpath', value='/html/body/div[2]/div/div[2]/div[2]/div/table[1]/tbody/tr/td[2]/table').text.split('\n')
          year=''
          for line in descript:
            if line.startswith('Название:'):
                book_name = line[10:]
            if line.startswith('Год издания:'):
                year = line[13:]
                break
          file_writer.writerow([f'{book_name},{year}'])
        except:
          continue
finally:
   f.close()
   drv.quit()
   input('press Enter')