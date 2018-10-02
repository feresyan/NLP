# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 20:29:43 2018

@author: feresyan
"""

import numpy
import io
from itertools import permutations

def read_file_init_table(fname):
    tag_count = {}
    tag_count['<start>'] = 0
    word_tag = {}
    tag_trans = {}
    dictionary = dict()

    with open(fname) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip().lower() for x in content]
    
    idx_line = 0
    is_first_word = 0
    
    while idx_line < len(content):
        prev_tag = '<start>'
        while not content[idx_line].startswith('</kalimat'):
            if  not content[idx_line].startswith('<kalimat'):
                content_part = content[idx_line].split('\t')
                if content_part[0] in dictionary:
                    if content_part[1] not in dictionary[content_part[0]]:
                        dictionary[content_part[0]].append(content_part[1])
                else:
                    dictionary[content_part[0]] = [content_part[1]] 
                if content_part[1] in tag_count:
                    tag_count[content_part[1]] += 1
                else:
                    tag_count[content_part[1]] = 1
                    
                current_word_tag = content_part[0]+','+content_part[1]
                if current_word_tag in word_tag:
                    word_tag[current_word_tag] += 1
                else:    
                    word_tag[current_word_tag] = 1
                    
                if is_first_word == 1:
                    current_tag_trans = '<start>,'+content_part[1]
                    is_first_word = 0
                else:
                    current_tag_trans = prev_tag+','+content_part[1]
                    
                if current_tag_trans in tag_trans:
                    tag_trans[current_tag_trans] += 1
                else:
                    tag_trans[current_tag_trans] = 1                    
                prev_tag = content_part[1]   
                
            else:
                tag_count['<start>'] += 1
                is_first_word = 1
            idx_line = idx_line + 1

        idx_line = idx_line+1 
    return tag_count, word_tag, tag_trans,dictionary

tag_count, word_tag, tag_trans, dictionary = read_file_init_table('sample.txt')
#print("TAG COUNT :")
#print(tag_count,"\n")
#print("WORD TAG :")
#print(word_tag,"\n")
#print("TAG TRANS:")
#print(tag_trans,"\n")
#print("DICTIONARY")
#print(dictionary,"\n")

def create_trans_prob_table(tag_trans, tag_count):
#    print(tag_trans)
    trans_prob = {}
    for tag1 in tag_count.keys():
        for tag2 in tag_count.keys():
            trans_idx = tag1+','+tag2
            if trans_idx in tag_trans:
                trans_prob[trans_idx] = tag_trans[trans_idx]/tag_count[tag1]
    return trans_prob

trans_prob = create_trans_prob_table(tag_trans, tag_count)
#print("Trans Prob:")
#print(trans_prob,"\n")

def create_emission_prob_table(word_tag, tag_count):
    emission_prob = {}
    for word_tag_entry in word_tag.keys():
        koma = 0
        if word_tag_entry[0] == ',':
            current_word = word_tag_entry[0]
            current_tag = word_tag_entry[2]
        else:
            for i in range(len(word_tag_entry)):
                if word_tag_entry[i] == ',':
                    koma = koma+1
            if koma > 1:
                current_word = word_tag_entry.rsplit(',',1)[0]
                current_tag = word_tag_entry.rsplit(',',1)[1]
#                print(first)
            else:
                word_tag_split = word_tag_entry.split(',')
                current_word = word_tag_split[0]
                current_tag = word_tag_split[1]
            
        emission_key = current_word+','+current_tag
        emission_prob[emission_key] = word_tag[word_tag_entry]/tag_count[current_tag]
    return emission_prob

emission_prob = create_emission_prob_table(word_tag,tag_count)
#print("EMISSION PROB :")
#print(emission_prob,"\n")

def data_tes(file_name):
    sentence = []
    sentence.append("<start>")
    sentences = []
    true_result = []
    true_results = []

    with open(file_name) as f:
        content = f.readlines()
        content = [x.strip() for x in content]
#        print(content)
        
    idx_line = 0
    
    while idx_line < len(content):
        if not content[idx_line].startswith('</kalimat'):
            if  not content[idx_line].startswith('<kalimat'):
                kata = content[idx_line].split('\t')
                kata[0] = kata[0].lower()
                kata[1] = kata[1].lower()
                true_result.append(kata[0]+','+kata[1])
                sentence.append(kata[0]) #ambil kata tanpa tag
        else:
            true_results.append(true_result)
            sentence.append("<end>")
            sentences.append(sentence)
            sentence = []
            sentence.append("<start>")
            true_result = []
        idx_line = idx_line + 1
    return sentences,true_results
sentences, true_results = data_tes('data_tes.txt')
#print(sentences)

def viterbi(trans_prob, emission_prob, tag_count, sentences, dictionary):
    best_prob = 0
    result = []
    results = []
    for i in range(len(sentences)):
        print(sentences[i])
        for j in range(len(sentences[i])):
            if sentences[i][j] != "<start>":
                if sentences[i][j] in dictionary:
                    for k in range(len(dictionary[sentences[i][j]])):
                        kata = sentences[i][j]+","+dictionary[sentences[i][j]][k]
                        if kata in emission_prob:
                            print("INI EMMISION : ",kata," : ",emission_prob[kata])
            else:
                if sentences[i][j+1] in dictionary:
                    for k in range(len(dictionary[sentences[i][j+1]])):
                        start = "<start>,"+dictionary[sentences[i][j+1]][k]
                        kata = sentences[i][j+1]+","+dictionary[sentences[i][j+1]][k]
                        if start in trans_prob:
                            print("INI START",start," : ",trans_prob[start])
                        if kata in emission_prob:
                            print("INI EMMISION ADA START : ",kata," : ",emission_prob[kata])
                        prob = trans_prob[start] * emission_prob[kata]
                        if best_prob < prob:
                            best_tag = dictionary[sentences[i][j+1]][k]
                            best_prob = prob
            print(sentences[i][j]+","+best_tag)
#            result.append(sentences[i][j]+","+best_tag)
#            print(result)
        results.append(result)
        best_prob = 0
#viterbi_mat, tag_sequence = viterbi(trans_prob, emission_prob, tag_count, sentence)
viterbi(trans_prob, emission_prob, tag_count, sentences, dictionary)

    






