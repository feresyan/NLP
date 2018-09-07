from bs4 import BeautifulSoup
import requests
import json
import csv

class News:
    def __init__(self, url, title, description):
        self.url = url
        self.title = title
        self.description = description

def saveCrawl(craURL, craTitle, craDesc):
    crawlerSet = []
    for x in range(0, len(craURL)):
        news = News(craURL[x], craTitle[x], craDesc[x])
        crawlerSet.append(news)
    return crawlerSet

def nyokotisi(urlna):
    response = requests.get(urlna)
    soup = BeautifulSoup(response.text,'lxml')
    judul = soup.find('title').get_text()
    url = response.url
    tagberita = soup.find(id='article-detail-content')
    isiberita = tagberita.find_all('p')
    corpus = ""
    for baris in isiberita:
        if ("href" in baris):
            pass
        else:
            corpus += baris.get_text() + " "
    return corpus

def getTitle(crawTitle):
    setJudul = []
    for htmljudul in crawTitle:
        setJudul.append(htmljudul.get_text()) #(title, url)
    return setJudul

def getUrl(crawTitle):
    setUrl = []
    for htmljudul in crawTitle:
        setUrl.append(htmljudul['href']) #(title, url)
    return setUrl

def getDescription(crawJudul):
    isiBerita = []
    for urlna in crawJudul:
        isiBerita.append(nyokotisi(urlna))
    return isiBerita

def writeToCsv(name, data):
    file = open(name, 'w', newline='')
    with file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Title', 'Url', 'Berita'])
        for berita in data:
            writer.writerow([berita.title, berita.url, berita.description])

def crawl(url):
    # berita Terbar
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'lxml')
    clearna = soup.find('ul',id='load_terbaru_content')
    title = clearna.find_all('a', {"class": "title-content"})
    judul = getTitle(title)
    url = getUrl(title)
    # for htmljudul in title:
    #     judul.append([htmljudul.get_text(),htmljudul['href']])
    isiberita = getDescription(url)
    data = saveCrawl(url, judul, isiberita)
    # for judulna in judul:
    #     isiberita.append(nyokotisi(judulna[1]))
    return data
    # print(data[1].url)

def main():
    url1 = 'https://www.viva.co.id/berita'
    url2 = 'https://www.viva.co.id/digital'
    url3 = 'https://www.viva.co.id/gaya-hidup'
    url4 = 'https://www.viva.co.id/otomotif'
    url5 = 'https://www.viva.co.id/bola'
    url6 = 'https://www.viva.co.id/showbiz'
    url7 = 'https://www.viva.co.id/sport'
    # url8 = 'https://www.viva.co.id/vlix'
    url9 = 'https://www.viva.co.id/other'
    url10 = 'https://www.viva.co.id/sport'
    data1 = crawl(url1)
    data2 = crawl(url2)
    data3 = crawl(url3)
    data4 = crawl(url4)
    data5 = crawl(url5)
    data6 = crawl(url6)
    data7 = crawl(url7)
    # data8 = crawl(url8)
    data9 = crawl(url9)
    data10 = crawl(url10)
    writeToCsv('viva-berita.csv', data1)
    writeToCsv('viva-digital.csv', data2)
    writeToCsv('viva-gaya-hidup.csv', data3)
    writeToCsv('viva-otomotif.csv', data4)
    writeToCsv('viva-bola.csv', data5)
    writeToCsv('viva-showbiz.csv', data6)
    writeToCsv('viva-sport.csv', data7)
    # writeToCsv('viva-vlix.csv', data8)
    writeToCsv('viva-other.csv', data9)
    writeToCsv('viva-sport.csv', data10)

main()