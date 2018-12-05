# Algoritma Naive Bayes

import csv
import nltk
import numpy as np
import string
import re
from collections import Counter

# Algoritma Spelling Correction ========================================================

def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('katadasar_0.txt').read()))

def P(word, N=sum(WORDS.values())):
    # "Probability of `word`."
    return WORDS[word] / N

def correction(word):
    # "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word):
    # "Generate possible spelling corrections for word."
    print()
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words):
    # "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    # "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)] # [('', 'kemarin'), ('k', 'emarin'), ('ke', 'marin'), dst]
    deletes    = [L + R[1:]               for L, R in splits if R] # ['emarin', 'kmarin', 'kearin', dst]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1] # ['ekmarin', 'kmearin', 'keamrin', dst]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters] # ['aemarin', 'bemarin', 'cemarin', dst]
    inserts    = [L + c + R               for L, R in splits for c in letters] # ['akemarin', 'bkemarin', 'ckemarin', dst]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    # "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))



# Ekstrasi Fitur & Preprocessing ===================================================

data_pesan = []
data_label = []
par_tokens = []

with open('corpus_sastrawi.txt', 'r') as myfile:
    data = (myfile.readlines())

corpus = [i.replace("\n","") for i in data]

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
    temp = nltk.word_tokenize(row)
    temp = [word for word in temp if word not in string.punctuation] # PREPROCESSING 1 -> menghilangkan punctuation yang menjadi fitur
    par_tokens.append(temp)

normal = []
penipuan = []
promo = []

for i in range(len(data_label)): # mencari index dari data_label yang termasuk kedalam class nya masing - masing
    if (int(data_label[i]) == 0) :
        for j in range(len(par_tokens[i])):
            if (par_tokens[i][j] not in corpus):
                par_tokens[i][j] = correction(par_tokens[i][j])
            normal.append(par_tokens[i][j])
    elif (int(data_label[i]) == 1):
        penipuan.append(par_tokens[i])
    elif (int(data_label[i]) == 2):
        promo.append(par_tokens[i])

# ============================== Perhitungan Model menggunakan rumus naive bayes ========================================================

prob_label_0 ={}
prob_label_1 ={}
prob_label_2 ={}

def calculate_probability(vocabulary, class_word, unique_vocab):
    return (class_word.count(vocabulary) + 1) / (len(class_word) + len(unique_vocab)) # Rumus Naive Bayes

all_word = list(np.concatenate(par_tokens,axis=None)) # memasukan seluruh kata yang sudah di tokenize ke satu variabel (dari multidimensi menjadi 1 diemnsi)
vocabulary = list(set(np.concatenate(par_tokens,axis=None))) # mencari distinct word dari kata yang sudah di tokenize
all_word_normal = list(np.concatenate(normal,axis=None)) # memasukan seluruh kata yang sudah di tokenize ke satu variabel (dari multidimensi menjadi 1 diemnsi)
all_word_penipuan = list(np.concatenate(penipuan,axis=None))# memasukan seluruh kata yang sudah di tokenize ke satu variabel (dari multidimensi menjadi 1 diemnsi)
all_word_promo = list(np.concatenate(promo,axis=None)) # memasukan seluruh kata yang sudah di tokenize ke satu variabel (dari multidimensi menjadi 1 diemnsi)

print("total kata = ", len(all_word), "," ,"total vocabulary = " , len(vocabulary))

for i in range(len(vocabulary)):
    prob_label_0[vocabulary[i]] = calculate_probability(vocabulary[i],all_word_normal,vocabulary)

for i in range(len(vocabulary)):
    prob_label_1[vocabulary[i]] = calculate_probability(vocabulary[i],all_word_penipuan,vocabulary)

for i in range(len(vocabulary)):
    prob_label_2[vocabulary[i]] = calculate_probability(vocabulary[i],all_word_promo,vocabulary)

# print(prob_label_0)
# print(prob_label_1)
# print(prob_label_2)

# ============================================================== MODEL =========================================================================================================================================


# ============================================================== Pengujian

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

print(len(par_tokens_test))

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
            temp_1 *= calculate_probability(par_tokens_test[i][j], all_word_penipuan, vocabulary)
            temp_2 *= calculate_probability(par_tokens_test[i][j], all_word_promo, vocabulary)

    temp_0 *= prob_0
    temp_1 *= prob_1
    temp_2 *= prob_2

    print(temp_0,temp_1,temp_2)

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

print("accuracy = ", count/15)
