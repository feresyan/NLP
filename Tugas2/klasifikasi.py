#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 12:52:12 2018

@author: naive
"""

def read_dataset(fname):
    sentences = []
    tags = []
    with open(fname) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    idx_line = 0
    while idx_line < len(content):
        sent = []
        tag = []
#        print('idx_line =')
#        print(idx_line)
        while not content[idx_line].startswith('</kalimat'):
            if  not content[idx_line].startswith('<kalimat'):
                content_part = content[idx_line].split('\t')
                sent.append(content_part[0])
                tag.append(content_part[1])
            idx_line = idx_line + 1
        sentences.append(sent)
        tags.append(tag)
        idx_line = idx_line++2        
    return sentences, tags

#sentences,tags = read_dataset('sample_postagged.txt')
sentences,tags = read_dataset('data_tes2.txt')
print(sentences)

def features(sentence, index):
    """ sentence: [w1, w2, ...], index: the index of the word """
    return {
        'word': sentence[index],
        'prefix-1': sentence[index][0],
        'prefix-2': sentence[index][:2],
        'prefix-3': sentence[index][:3],
        'suffix-1': sentence[index][-1],
        'suffix-2': sentence[index][-2:],
        'suffix-3': sentence[index][-3:],
        'prev_word': '' if index == 0 else sentence[index - 1],
        'next_word': '' if index == len(sentence) - 1 else sentence[index + 1],
    }
    
def transform_to_dataset(sentences, tags):
    X, y = [], []
    for sentence_idx in range(len(sentences)):
        for index in range(len(sentences[sentence_idx])):
            X.append(features(sentences[sentence_idx], index))
            y.append(tags[sentence_idx][index])
 
    return X, y

# Split the dataset for training and testing
cutoff = int(.75 * len(sentences[0]))
training_sentences = sentences[0][:cutoff]
test_sentences = sentences[0][cutoff:]
training_tags = tags[0][:cutoff]
test_tags = tags[0][cutoff:]

print(cutoff)
print(training_sentences)
print(test_sentences)
print(training_tags)
print(test_tags)

X, y = transform_to_dataset(training_sentences, training_tags)
print("X : ",X)
print("y : ",y)
