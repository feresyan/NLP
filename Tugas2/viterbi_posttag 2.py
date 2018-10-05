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

emis_prob = create_emission_prob_table(word_tag,tag_count)
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


def viterbi(trans_prob, emis_prob, tag_count, sentences, dictionary):
    best_prob_kata = 0
    hasil = []
    result = []
    results = []
    tag = []
    for i in range(len(sentences)):
        print(sentences[i])
        for j in range(len(sentences[i])):
            print("kata : ",sentences[i][j])
            if sentences[i][j] == "<start>":
                probabilitas = 1
                tag_awal = "<start>"
            elif sentences[i][j] == "<end>":
                continue
            else:
                if sentences[i][j] in dictionary:
                    for k in range(len(dictionary[sentences[i][j]])):
                        print("TAG : ",dictionary[sentences[i][j]][k])
                        kata_dengan_tag = sentences[i][j]+","+dictionary[sentences[i][j]][k]
                        tag_baru = dictionary[sentences[i][j]][k]
                        transition = tag_awal+","+tag_baru
                        if transition in trans_prob:
                            transition_prob = trans_prob[transition]
                        else:
                            transition_prob = 0
                        if kata_dengan_tag in emis_prob:
                            emission_prob = emis_prob[kata_dengan_tag]
                        else:
                            emission_prob= 0
                        print("Probabilitas : ",probabilitas)
                        print("transition : ",transition_prob)
                        print("emmision : ",emission_prob)
                        best_prob = probabilitas*transition_prob*emission_prob
                        print("probabilitas baru : ",best_prob)
                        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
                        hasil.append(best_prob)
                        tag.append(tag_baru)
                    for l in range(len(hasil)):
                        if hasil[l] > best_prob_kata:
                            best_prob_kata = hasil[l]
                            probabilitas = hasil[l]
                            tag_awal = tag[l]
                    kata = sentences[i][j]+","+tag_awal
                    print("hasil kata :",kata)
                    result.append(kata)
                    best_prob_kata = 0
                    print("----------------------------")
                    tag = []
                    hasil = []
                else:
                    kata = sentences[i][j]+",z"
                    result.append(kata)
        print(result)
        print("----------------------------")
        results.append(result)
        result = []
    return results

results =  viterbi(trans_prob, emis_prob, tag_count, sentences, dictionary)
#print(true_results)

def cek(results,true_results):
    sama = 0
    for i in range(len(results)):
        counter = 0
#        print("LEN RESULTS :",len(results[i]))
        print("results : True Result")
        print("---------------------")
        for j in range(len(results[i])):
            print(results[i][j]," : ",true_results[i][j])
            if results[i][j] == true_results[i][j]:
                counter= counter+1
        if counter == len(results[i]):
            print("Sama\n")
            sama = sama+1
        else:
            print("Tidak Sama\n")
    return sama

sama = cek(results,true_results)

def akurasi(sama,results):
    print(len(results))
    acc = (sama / len(results))*100
    return acc

acc = akurasi(sama,results)
print("Akurasi Baseline Posttag : ",acc,"%")





