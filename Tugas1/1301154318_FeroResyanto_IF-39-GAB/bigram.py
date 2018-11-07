import csv
import nltk
import re
import math

#inisiasi variabel yang digunakan
list_berita = []
freq_tab = {}
total_count = 0
bigram = {}
bigram_count = 0
prob_tab = {}

# Ambil artikel lalu masukan ke dalam list berita
with open('artikel/viva-berita.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    for row in readCSV:
        berita = row[0]+' '+row[2]
        berita = berita.lower()
        list_berita.append(berita)
with open('artikel/viva-bola.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    for row in readCSV:
        berita = row[0]+' '+row[2]
        berita = berita.lower()
        list_berita.append(berita)
with open('artikel/viva-digital.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    for row in readCSV:
        berita = row[0]+' '+row[2]
        berita = berita.lower()
        list_berita.append(berita)
with open('artikel/viva-gaya-hidup.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    for row in readCSV:
        berita = row[0]+' '+row[2]
        berita = berita.lower()
        list_berita.append(berita)
with open('artikel/viva-other.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    for row in readCSV:
        berita = row[0]+' '+row[2]
        berita = berita.lower()
        list_berita.append(berita)
with open('artikel/viva-otomotif.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    for row in readCSV:
        berita = row[0]+' '+row[2]
        berita = berita.lower()
        list_berita.append(berita)
with open('artikel/viva-showbiz.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    for row in readCSV:
        berita = row[0]+' '+row[2]
        berita = berita.lower()
        list_berita.append(berita)
with open('artikel/viva-sport.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    for row in readCSV:
        berita = row[0]+' '+row[2]
        berita = berita.lower()
        list_berita.append(berita)
with open('artikel/viva-berita2.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    for row in readCSV:
        berita = row[0]+' '+row[2]
        berita = berita.lower()
        list_berita.append(berita)
with open('artikel/viva-sport2.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    for row in readCSV:
        berita = row[0]+' '+row[2]
        berita = berita.lower()
        list_berita.append(berita)

# Melakukan tokenisasi untuk setiap artikel, lalu menghitung frekuensi kata dari seluruh artikel
for berita in list_berita:
    berita = re.sub('[^a-zA-Z]',' ', berita) #Menghilangkan angka,tanda baca dan simbol pada artikel
    token_berita = nltk.word_tokenize(berita) #Melakukan tokenisasi pada artikel
    for token in token_berita:
        if token in freq_tab:
            freq_tab[token] += 1
        else:
            freq_tab[token] = 1
        total_count +=1

#melakukan bigram pada setiap artikel
for berita in list_berita:
    berita = re.sub('[^a-zA-Z]',' ', berita) #Menghilangkan angka,tanda baca dan simbol pada artikel
    token_berita = nltk.word_tokenize(berita) #Melakukan tokenisasi pada artikel
    length_token_berita = len(token_berita)
    for x in range(0, length_token_berita - 1):
        if token_berita[x] in bigram:
            if token_berita[x + 1] in bigram[token_berita[x]]:
                bigram[token_berita[x]][token_berita[x + 1]] += 1
            else:
                bigram[token_berita[x]][token_berita[x + 1]] = 1
                bigram_count += 1
        else:
            bigram[token_berita[x]] = {}
            bigram[token_berita[x]][token_berita[x + 1]] = 1
            bigram_count += 1

#Menghitung probabilitas pada kata 
for x in bigram:
#     print('---------------------------------------')
#     print(x, bigram[x],'\n')
    prob_tab[x] = {}
    for y in bigram[x]:
#         print(y, bigram[x][y])
        prob_tab[x][y] = bigram[x][y]/freq_tab[x]
#         print('Probabilty :',prob)
#         print('\n')

#pengujian prediksi kemunculan terhadap 10 kata
kata_uji = ['bagi','mereka','alasan','saat','mengatakan','tidak','bisa','saya','prabowo','joko']
hasil = 0
kata_selanjutnya = ''

# print(bigram['joko'])
for x in kata_uji:
    hasil = 0
    kata_selanjutnya = ''
    for y in bigram[x]:
        if bigram[x][y] > hasil:
            hasil = bigram[x][y]
            kata_selanjutnya = y
    print('Kata :',x)
    print('Kata Selanjutnya :',kata_selanjutnya)
    print('Jumlah kemunculan kalimat',x,kata_selanjutnya,':',hasil)
    print('---------------------------------')

#Evaluasi model dengan perplexity menggunakan 5 kalimat
kalimat = ['Kalau Deddy Mizwar Keluar Kita Ucapkan Selamat Jalan',
           'Sandiaga Ajak Presiden Jokowi Tukarkan Dolar AS ke Rupiah',
           'Erick Thohir Masuk Top List Calon Ketua Timses Jokowi',
           'Pertamina Mulai Kelola Blok SES',
           'Luhut Pastikan Proyek Kelistrikan Ditunda']
for kal in kalimat:
    kal = kal.lower()
    tokens = nltk.word_tokenize(kal)
    total_prob = 1.0
    for i in range(0,len(tokens)-1):
        print('kata 1 : ',tokens[i])
        print('kata 2 : ',tokens[i+1])
        print('Probabilitas : ',prob_tab[tokens[i]][tokens[i+1]])
        total_prob = total_prob * prob_tab[tokens[i]][tokens[i+1]]
    print('total probabilitas kalimat : ',total_prob)
    total_prob = 1/total_prob
    i = 1/(i+1)
    print('Preplexity: ',math.pow(total_prob,i),'\n')
     

   
        
        
        
        
        
        
        
        