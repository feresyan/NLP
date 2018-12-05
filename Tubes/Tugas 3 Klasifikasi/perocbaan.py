# Algoritma Naive Bayes

import csv
import nltk
import numpy as np
import string

data_pesan = []
data_label = []
par_tokens = []

with open('corpus_sastrawi.txt', 'r') as myfile:
    data = (myfile.readlines())

corpus = [i.replace("\n", "") for i in data]

# Ambil pesan lalu masukan ke dalam list pesan
with open('dataset_sms_spam _v1.csv',
          encoding='utf-8') as csvfile:  # encoding='utf-8' digunakan karena dalam csv secara default, file akan di-decode kedalam unicode (contoh : emoticon akan didecode menjadi unicode) sehingga akan menyebabkan error. Using encoding utf-8 for commonly encoder
    readCSV = csv.reader(csvfile, delimiter=',')
    next(readCSV)  # meng-skip row pertama dalam .csv dataset
    for row in readCSV:
        pesan = row[0]
        pesan = pesan.lower()
        label = row[1]

        data_pesan.append(pesan)
        data_label.append(label)
for row in data_pesan:
    par_tokens.append(nltk.word_tokenize(row))

all_word = list(np.concatenate(par_tokens,axis=None))

print("0 :", all_word)

all_word = [word for word in all_word if word not in string.punctuation]

word_feature = []
word_feature2 = []

for word in all_word:
    if word in corpus:
        word_feature.append(word)
    else:
        word_feature2.append(word)



print("0.1 : ", word_feature)
print("0.2 : ", word_feature2)



# normal = []
# penipuan = []
# promo = []
#
# for i in range(len(data_label)):  # mencari index dari data_label yang termasuk kedalam class nya masing - masing
#     if (int(data_label[i]) == 0):
#         normal.append(par_tokens[i])
#     elif (int(data_label[i]) == 1):
#         penipuan.append(par_tokens[i])
#     elif (int(data_label[i]) == 2):
#         promo.append(par_tokens[i])

# ============================== Tokenize and classification word to array class ===========================

# promo = list(np.concatenate(promo, axis=None))
#
# print(promo)
#
# promo = [word for word in promo if word not in string.punctuation]
#
# print(promo)
#
# # temp_link = [word for word in promo if word[:6] == "http//" or word[:2] =="//"]
#
# temp = "makan"
#
# if temp in corpus:
#     print(temp)
#
# # ============================== Preprocessing word ========================================================
#
# prob_label_0 = {}
# prob_label_1 = {}
# prob_label_2 = {}
#
#
# def calculate_probability(vocabulary, class_word, all_word):
#     return (class_word.count(vocabulary) + 1) / (len(all_word) + len(vocabulary))  # Rumus Naive Bayes
#
#
# all_word = list(np.concatenate(par_tokens,axis=None))  # memasukan seluruh kata yang sudah di tokenize ke satu variabel (dari multidimensi menjadi 1 diemnsi)
# vocabulary = list(set(np.concatenate(par_tokens, axis=None)))  # mencari distinct word dari kata yang sudah di tokenize
# all_word_normal = list(np.concatenate(normal,axis=None))  # memasukan seluruh kata yang sudah di tokenize ke satu variabel (dari multidimensi menjadi 1 diemnsi)
# all_word_penipuan = list(np.concatenate(penipuan,axis=None))  # memasukan seluruh kata yang sudah di tokenize ke satu variabel (dari multidimensi menjadi 1 diemnsi)
# all_word_promo = list(np.concatenate(promo, axis=None))  # memasukan seluruh kata yang sudah di tokenize ke satu variabel (dari multidimensi menjadi 1 diemnsi)
#
# print("total kata = ", len(all_word), ",", "total vocabulary = ", len(vocabulary))
#
# for i in range(len(vocabulary)):
#     prob_label_0[vocabulary[i]] = calculate_probability(vocabulary[i], all_word_normal, all_word)
#
# for i in range(len(vocabulary)):
#     prob_label_1[vocabulary[i]] = calculate_probability(vocabulary[i], all_word_penipuan, all_word)
#
# for i in range(len(vocabulary)):
#     prob_label_2[vocabulary[i]] = calculate_probability(vocabulary[i], all_word_promo, all_word)
#
# # print(prob_label_0)
# # print(prob_label_1)
# # print(prob_label_2)

# ============================================================== MODEL =========================================================================================================================================