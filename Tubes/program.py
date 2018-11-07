#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 12:42:44 2018

@author: naive
"""

import csv
import nltk
import re
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

nltk.download('punkt')

data_pesan = []
data_label = []
freq_tab = {}

        
# Ambil pesan lalu masukan ke dalam list pesan
with open('dataset_sms_spam _v1.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        pesan = row[0]
        pesan = pesan.lower()
        label = row[1]
        
        #Pre-Processing
        #character removal
        pesan = re.sub('[!&%@#$?:;,.0123456789*/-]', '', pesan)
        pesan = re.sub('()', '', pesan)
        
        #URL removal
        pesan = re.sub(r'^https?:\/\/.*[\r\n]*', '', pesan, flags=re.MULTILINE)
        
        #Stopword bahasa indonesia sastrawi
        factory = StopWordRemoverFactory()
        stopword = factory.create_stop_word_remover()
        pesan = stopword.remove(pesan)
        
        data_pesan.append(pesan)
        data_label.append(label)

for row in data_pesan:
    par_tokens = nltk.word_tokenize(row)
    print(par_tokens)
    
    
    