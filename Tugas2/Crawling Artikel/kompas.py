import requests
import csv
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()

header = {'user-agent':ua.chrome}

date = time.strftime("%Y-%m-%d")

url = ('http://nasional.kompas.com/search/'+date)

kompas_page = requests.get(url,headers = header)

soup = BeautifulSoup(kompas_page.content,'lxml')

i = 0

for pagingwrap in soup.findAll('div', {'class': 'paging__wrap clearfix'}):  #pagination
    for pagingitem in pagingwrap.findAll('div', {'class': 'paging__item'}):
        for linkpaging in pagingitem.findAll('a', {'class': 'paging__link'}, href = True):
            linkpagingg = linkpaging['href']

last_link = linkpagingg.split('/')
jumlah_last_link = int(last_link[5])

csvfiles = open('kompas.csv','w')

for page in range (1, jumlah_last_link):
    page_fix = str(page)
    url_next = ('http://nasional.kompas.com/search/'+date+'/'+page_fix)
    kompas_page_next = requests.get(url_next,headers = header)
    soup2 = BeautifulSoup(kompas_page_next.content,'lxml')
    for divlistberita in soup2.findAll('div', {'class': 'article__list clearfix'}):
        for divlisttitle in divlistberita.findAll('div', {'class': 'article__list__title'}):
            for divtitlemedium in divlisttitle.findAll('h3', {'class': 'article__title article__title--medium'}):
                for judullink in divtitlemedium.findAll('a', {'class' : 'article__link'}, href = True):
                    csvfiles.write(judullink.string)
                    for divlistinfo in divlistberita.findAll('div', {'class': 'article__list__info'}):
                        for tanggalberita in divlistinfo.findAll('div', {'class': 'article__date'}):
                            csvfiles.write(tanggalberita.string)
                            for kategoriberita in divlistinfo.findAll('div',{'class': 'article__subtitle--inline'}):
                                csvfiles.write(kategoriberita.text)
                                all_links = [judullink['href']]

                                for single_link in all_links:
                                    final_page = requests.get(single_link)
                                    final_soup = BeautifulSoup(final_page.content, 'lxml')
                                    for class_content in final_soup.findAll('div', {'class': 'col-bs9-7'}):
                                        for read_content in class_content.findAll('div', {'class': 'read__content'}):
                                            csvfiles.write(str(read_content))
csvfiles.close()