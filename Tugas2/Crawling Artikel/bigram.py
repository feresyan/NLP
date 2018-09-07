import csv
import nltk

list_berita = []
freq_tab = {}
total_count = 0
prob_tab = {}

with open('viva-berita.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    for row in readCSV:
        berita = row[0]+' '+row[2]
        berita = berita.lower()
        list_berita.append(berita)
with open('viva-bola.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    for row in readCSV:
        berita = row[0]+' '+row[2]
        berita = berita.lower()
        list_berita.append(berita)

# for berita in list_berita:
#     token_berita = nltk.word_tokenize(berita)
#     for token in token_berita:
#         if token in freq_tab:
#             freq_tab[token] += 1
#         else:
#             freq_tab[token] = 1
#         total_count +=1
# print(freq_tab)

for berita in list_berita:
    bigram = {}
    bigram_count = 0
    token_berita = nltk.word_tokenize(berita)
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
    print(bigram)
    print(bigram_count)
        

     

   
        
        
        
        
        
        
        
        