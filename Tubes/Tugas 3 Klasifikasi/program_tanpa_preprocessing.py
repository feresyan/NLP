# Algoritma Naive Bayes

import csv
import nltk
import numpy as np


# Ekstrasi Fitur & Preprocessing =========================================================================================

data_pesan = []
data_label = []
par_tokens = []

# Ambil pesan lalu masukan ke dalam list pesan
with open('dataset_sms_spam _v1.csv', encoding='utf-8') as csvfile: # encoding='utf-8' digunakan karena dalam csv secara default, file akan di-decode kedalam unicode (contoh : emoticon akan didecode menjadi unicode) sehingga akan menyebabkan error. Using encoding utf-8 for commonly encoder
    readCSV = csv.reader(csvfile, delimiter=',')
    next(readCSV) # meng-skip row pertama dalam .csv dataset
    for row in readCSV:
        pesan = row[0]
        pesan = pesan.lower() # PREPROCESSING melakukan case folding agar seluruh karakter kata menjadi huruf kecil
        label = row[1]

        data_pesan.append(pesan)
        data_label.append(label)

for row in data_pesan:
    par_tokens.append(nltk.word_tokenize(row)) # FEATURE SELECTION 1 -> mentokenisasi kata agar dapa dihitung jumlah kemunculan kata tersebut untuk perhitungan klasifikasi

normal = []
penipuan = []
promo = []


for i in range(len(data_label)): # mencari nilai label sebenarnya pada par_tokens yang termasuk kedalam class nya masing - masing
    if (int(data_label[i]) == 0) :
        normal.append(par_tokens[i])
    elif (int(data_label[i]) == 1):
        penipuan.append(par_tokens[i])
    elif (int(data_label[i]) == 2):
        promo.append(par_tokens[i])


# Perhitungan Model menggunakan rumus naive bayes =================================================================================

prob_label_0 ={}
prob_label_1 ={}
prob_label_2 ={}

def calculate_probability(vocabulary, class_word, unique_vocab):
    return (class_word.count(vocabulary) + 1) / (len(class_word) + len(unique_vocab)) # Rumus Naive Bayes

all_word = list(np.concatenate(par_tokens,axis=None)) # memasukan seluruh kata yang sudah di tokenize ke satu variabel (dari multidimensi menjadi 1 dimensi)
vocabulary = list(set(np.concatenate(par_tokens,axis=None))) # mencari distinct word dari kata yang sudah di tokenize dengan function 'set'
all_word_normal = list(np.concatenate(normal,axis=None)) # memasukan seluruh kata yang sudah di tokenize ke satu variabel (dari multidimensi menjadi 1 dimensi)
all_word_penipuan = list(np.concatenate(penipuan,axis=None))# memasukan seluruh kata yang sudah di tokenize ke satu variabel (dari multidimensi menjadi 1 dimensi)
all_word_promo = list(np.concatenate(promo,axis=None)) # memasukan seluruh kata yang sudah di tokenize ke satu variabel (dari multidimensi menjadi 1 dimensi)

print("total kata = ", len(all_word), "," ,"total vocabulary = " , len(vocabulary))

for i in range(len(vocabulary)):
    prob_label_0[vocabulary[i]] = calculate_probability(vocabulary[i], all_word_normal, vocabulary)
    prob_label_1[vocabulary[i]] = calculate_probability(vocabulary[i], all_word_penipuan, vocabulary)
    prob_label_2[vocabulary[i]] = calculate_probability(vocabulary[i], all_word_promo,vocabulary)

# ============================================================== MODEL =========================================================================================================================================

# ============================================================== Pengujian ===============================================================

prob_0 = len(normal) / len(data_label)
prob_1 = len(penipuan) / len(data_label)
prob_2 = len(promo) / len(data_label)

data_pesan_test = []
data_label_test = []
par_tokens_test = []

# Ambil pesan lalu masukan ke dalam list pesan
with open('datauji_sms_spam_v1.csv', encoding='utf-8') as csvfile: # encoding='utf-8' digunakan karena dalam csv secara default, file akan di-decode kedalam unicode (contoh : emoticon akan didecode menjadi unicode) sehingga akan menyebabkan error. Using encoding utf-8 for commonly encoder
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        pesan = row[0]
        pesan = pesan.lower()
        label = row[1]

        data_pesan_test.append(pesan)
        data_label_test.append(label)

for row in data_pesan_test:
    par_tokens_test.append(nltk.word_tokenize(row))


hasil = []

temp_0 = 1
temp_1 = 1
temp_2 = 1

for i in range(len(par_tokens_test)):
    for j in range(len(par_tokens_test[i])):
        try:
            temp_0 *= prob_label_0[par_tokens_test[i][j]]
            temp_1 *= prob_label_1[par_tokens_test[i][j]]
            temp_2 *= prob_label_2[par_tokens_test[i][j]]
        except:
            temp_0 *= calculate_probability(par_tokens_test[i][j],all_word_normal,vocabulary)
            temp_1 *= calculate_probability(par_tokens_test[i][j], all_word_penipuan,vocabulary)
            temp_2 *= calculate_probability(par_tokens_test[i][j], all_word_promo,vocabulary)

    temp_0 *= prob_0
    temp_1 *= prob_1
    temp_2 *= prob_2

    # print(temp_0,temp_1,temp_2)

    if (temp_0 > temp_1):
        if (temp_0 > temp_2):
            hasil.append(0)
        else :
            hasil.append(2)
    else:
        if (temp_1 > temp_2):
            hasil.append(1)
        else:
            hasil.append(2)

    temp_0 = 1
    temp_1 = 1
    temp_2 = 1

count = 0

for i in range(15):
    data_label_test[i] = int(data_label_test[i])
    if hasil[i] == data_label_test[i]:
        count += 1

print("prediksi : ", hasil)
print("actual   : ", data_label_test)
print("jumlah benar : ",count, "/ 15",)
print("accuracy = ", count/15)








