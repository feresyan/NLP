# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 09:30:03 2018

@author: feresyan
"""

def read_file_init_table(fname):
    word_tag = {}
    words = dict()
    with open(fname) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]

    idx_line = 0
    
    while idx_line < len(content):
        while not content[idx_line].startswith('</kalimat'):
            if  not content[idx_line].startswith('<kalimat'):
                content_part = content[idx_line].split('\t')
                content_part[0] = content_part[0].lower()
                content_part[1] = content_part[1].lower()
                current_word_tag = content_part[0]+','+content_part[1]
                if current_word_tag in word_tag:
                    word_tag[current_word_tag] += 1
                else: 
                    word_tag[current_word_tag] = 1
                if content_part[0] in words:
                    if content_part[1] not in words[content_part[0]]:
                        words[content_part[0]].append(content_part[1])
                else:
                    words[content_part[0]] = [content_part[1]]                   
            idx_line = idx_line + 1
        idx_line = idx_line+1 
    return word_tag,words

word_tag,words= read_file_init_table('data_training.txt')
#print("WORD TAG :")
#print(word_tag,"\n")
#print("words")
#print(words,"\n")

def data_tes(file_name):
    sentence = []
    sentences = []
    true_result = []
    true_results = []

    with open(file_name) as f:
        content = f.readlines()
        content = [x.strip() for x in content]
        
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
            sentences.append(sentence)
            sentence = []
            true_result = []
        idx_line = idx_line + 1
    return sentences,true_results
sentences, true_results = data_tes('data_tes.txt')
#print(sentences,"\n")
#print(true_results,"\n")

def baseline(sentences,word_tag,words):
    result = []
    results = []
    for i in range(len(sentences)):
        for j in range(len(sentences[i])):
            best = 0
            if sentences[i][j] in words:
                for k in range(len(words[sentences[i][j]])):
                    kata = sentences[i][j]+","+words[sentences[i][j]][k]
                    if kata in word_tag:
                        if word_tag[kata] > best:
                            best = word_tag[kata]
                            tag = words[sentences[i][j]][k]
 
                result.append(sentences[i][j]+','+tag)
            else:
                result.append(sentences[i][j]+',nn')
        results.append(result)
        result = []
    return results
    
results = baseline(sentences,word_tag,words)
#print(results)

def cek(results,true_results):
#    sama = 0
    jml_kata = 0
    counter = 0
    for i in range(len(results)):
#        counter = 0
        print("results : True Result")
        print("---------------------")
        for j in range(len(results[i])):
            print(results[i][j]," : ",true_results[i][j])
            if results[i][j] == true_results[i][j]:
                counter= counter+1
            jml_kata +=1
#        if counter == len(results[i]):
#            print("Sama\n")
#            sama = sama+1
#        else:
#            print("Tidak Sama\n")
    print(counter)
    print(jml_kata)
    return counter,jml_kata
    
counter, jml_kata =cek(results,true_results)

def akurasi(counter,jml_kata):
    acc = (counter / jml_kata)*100
    return acc

acc = akurasi(counter,jml_kata)
print("Akurasi Baseline Posttag : ",acc,"%")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    