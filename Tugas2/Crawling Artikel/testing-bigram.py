# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 19:25:19 2018

@author: feresyan
"""

import nltk

bigram = {}
bigram_count = 0
kalimat = "demokrat: kalau deddy mizwar keluar, kita ucapkan selamat jalan viva – partai demokrat menyatakan tak masalah untuk melepas kadernya yang tak sama sikap politiknya dalam arah dukungan pilpres 2019."
tkn_kalimat = nltk.word_tokenize(kalimat)
length = len(tkn_kalimat)
for x in range(0, length - 1):
    if tkn_kalimat[x] in bigram:
        if tkn_kalimat[x + 1] in bigram[tkn_kalimat[x]]:
            print(x)
            bigram[tkn_kalimat[x]][tkn_kalimat[x + 1]] += 1
            print('masuk sini')
            print(bigram)
        else:
            print(x)
            print('masuk sana')
            print(tkn_kalimat[x])
            print(tkn_kalimat[x+1])
            bigram[tkn_kalimat[x]][tkn_kalimat[x + 1]] = 1
            bigram_count += 1
            print(bigram)
    else:
        print(x)
        print('masuk depan')
        bigram[tkn_kalimat[x]] = {}
        bigram[tkn_kalimat[x]][tkn_kalimat[x + 1]] = 1
        print(bigram)
        bigram_count += 1
print(bigram)
print(bigram_count)  

#import pandas as pd

#xl= pd.ExcelFile("berita.xlsx")
#dataset = label_to_binary(xl.parse("viva-berita"))
#print(dataset)