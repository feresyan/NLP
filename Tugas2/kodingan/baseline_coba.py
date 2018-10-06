# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 16:54:44 2018

@author: feresyan
"""

training_sentences = []
training_tags = [] 
test_sentences = []
tets_tags = []

#Membaca file
def read_file_train_init_table(fname):
    words = []
    tags = []
    with open(fname) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    idx_line = 0
    
    while idx_line < len(content):
        word = []
        tag = []
        while not content[idx_line].startswith('</kalimat'):
            if not content[idx_line].startswith('<kalimat'):
                content_part = content[idx_line].split('\t')
                word.append(content_part[0].lower())
                tag.append(content_part[1])
            idx_line = idx_line + 1
        words.append(word)
        tags.append(tag)
        idx_line = idx_line + 2
    return words, tags

words,tags = read_file_train_init_table('data_training.txt')
training_sentences = words
training_tags = tags

words,tags = read_file_train_init_table('data_tes.txt')
test_sentences = words
tets_tags = tags

#Menghitung frekuensi tag untuk setiap kata
def word_tag(words, tags):
    word_tags = {}
    for word,tag in zip(words,tags):
        for wr,tg in zip(word,tag):
            if wr in word_tags:
                if tg in word_tags[wr]:
                    word_tags[wr][tg] += 1
                else:
                    word_tags[wr][tg] = 1
            else:
                word_tags[wr] = {}
                word_tags[wr][tg] = 1
    return word_tags
word_tag = word_tag(training_sentences,training_tags)
#print("Word Tag : ")
#print("-----------")
#print(word_tag)

#Memilih tag yang terbesar untukk setiap kata
import operator
def baseline(word_tags):
    baseline = {}
    for key, value in word_tags.items():
        baseline[key] = max(value.items(), key=operator.itemgetter(1))[0]
    return baseline
max_frekuensi_tag = baseline(word_tag)
#print("Kata dan postag berdasarkan frekuensi terbanyak :")
#print("-------------------------------------------------")
#print(max_frekuensi_tag)

#Menghitung akurasi
def accuracy(test_sentences, test_tags, max_frekuensi_tag):
    accuracy = 0
    count_word = 0
    for i in range(len(test_sentences)):
        for j in range(len(test_sentences[i])):
            if test_sentences[i][j] in max_frekuensi_tag:
                if test_tags[i][j] == max_frekuensi_tag[test_sentences[i][j]]:
                     accuracy += 1  
            count_word += 1
    
    print("Akurasi : ",(accuracy/count_word)*100)
accuracy(test_sentences, test_tags, max_frekuensi_tag)