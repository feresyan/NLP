# Algoritma Naive Bayes

import csv
import nltk
import numpy as np

data_pesan = []
data_label = []
par_tokens = []

# Ambil pesan lalu masukan ke dalam list pesan
with open('dataset_sms_spam _v1.csv', encoding='utf-8') as csvfile: # encoding='utf-8' digunakan karena dalam csv secara default, file akan di-decode kedalam unicode (contoh : emoticon akan didecode menjadi unicode) sehingga akan menyebabkan error. Using encoding utf-8 for commonly encoder
    readCSV = csv.reader(csvfile, delimiter=',')
    next(readCSV) # meng-skip row pertama dalam .csv dataset
    for row in readCSV:
        pesan = row[0]
        pesan = pesan.lower()
        label = row[1]

        data_pesan.append(pesan)
        data_label.append(label)

for row in data_pesan:
    par_tokens.append(nltk.word_tokenize(row)) #Melakukan tokenize pada data pesan dan dimasukan kedalam variabel par_tokens

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

# ============================== Tokenize and classification word to array class ==================================

prob_label_0 ={}
prob_label_1 ={}
prob_label_2 ={}

def calculate_probability(vocabulary, class_word, all_word):
	return (class_word.count(vocabulary) + 1) / (len(all_word) + len(vocabulary)) # Rumus Naive Bayes

all_word = list(np.concatenate(par_tokens,axis=None)) # memasukan seluruh kata yang sudah di tokenize ke satu variabel (dari multidimensi menjadi 1 dimensi)
vocabulary = list(set(np.concatenate(par_tokens,axis=None))) # mencari distinct word dari kata yang sudah di tokenize dengan function 'set'
all_word_normal = list(np.concatenate(normal,axis=None)) # memasukan seluruh kata yang sudah di tokenize ke satu variabel (dari multidimensi menjadi 1 dimensi)
all_word_penipuan = list(np.concatenate(penipuan,axis=None))# memasukan seluruh kata yang sudah di tokenize ke satu variabel (dari multidimensi menjadi 1 dimensi)
all_word_promo = list(np.concatenate(promo,axis=None)) # memasukan seluruh kata yang sudah di tokenize ke satu variabel (dari multidimensi menjadi 1 dimensi)

print(all_word_normal)

print("total kata = ", len(all_word), "," ,"total vocabulary = " , len(vocabulary))

for i in range(len(vocabulary)):
	prob_label_0[vocabulary[i]] = calculate_probability(vocabulary[i],all_word_normal,all_word)

for i in range(len(vocabulary)):
    prob_label_1[vocabulary[i]] = calculate_probability(vocabulary[i],all_word_penipuan,all_word)

for i in range(len(vocabulary)):
    prob_label_2[vocabulary[i]] = calculate_probability(vocabulary[i],all_word_promo,all_word)

# print(prob_label_0)
# print(prob_label_1)
# print(prob_label_2)

# ======================================================= MODEL ====================================================

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

# print(len(par_tokens_test))

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
            temp_0 *= calculate_probability(par_tokens_test[i][j],all_word_normal,all_word)
            temp_1 *= calculate_probability(par_tokens_test[i][j], all_word_penipuan, all_word)
            temp_2 *= calculate_probability(par_tokens_test[i][j], all_word_promo, all_word)

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
    if hasil[i] == int(data_label_test[i]):
        count += 1

# print(hasil)
# print(data_label_test)
# print(count)
# print("accuracy = ", count/15)








