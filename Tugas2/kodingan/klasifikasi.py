#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 12:52:12 2018

@author: feresyan
"""

def read_dataset(fname):
    training_sentences = []
    training_tags = []
    with open(fname) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    idx_line = 0
    while idx_line < len(content):
        sent = []
        tag = []
        while not content[idx_line].startswith('</kalimat'):
            if  not content[idx_line].startswith('<kalimat'):
                content_part = content[idx_line].split('\t')
                sent.append(content_part[0])
                tag.append(content_part[1])
            idx_line = idx_line + 1
        training_sentences.append(sent)
        training_tags.append(tag)
        idx_line = idx_line++2        
    return training_sentences, training_tags

training_sentences,training_tags = read_dataset('data_training.txt')
print(len(training_sentences))

def read_dataTest(fname):
    test_sentences = []
    test_tags = []
    with open(fname) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    idx_line = 0
    while idx_line < len(content):
        sent = []
        tag = []
        while not content[idx_line].startswith('</kalimat'):
            if  not content[idx_line].startswith('<kalimat'):
                content_part = content[idx_line].split('\t')
                sent.append(content_part[0])
                tag.append(content_part[1])
            idx_line = idx_line + 1
        test_sentences.append(sent)
        test_tags.append(tag)
        idx_line = idx_line++2        
    return test_sentences, test_tags

test_sentences,test_tags = read_dataTest('data_tes.txt')
#print(len(test_sentences))

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

X, y = transform_to_dataset(training_sentences, training_tags)
print('data training ke-4 =')
print(X[3])
print('label training ke-4 =')
print(y[3])

from sklearn import tree
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline
 
clf = Pipeline([
    ('vectorizer', DictVectorizer(sparse=False)),
    ('classifier', tree.DecisionTreeClassifier(criterion='entropy'))
])
clf.fit(X, y)   
 
print('Training completed') 

X_test, y_test = transform_to_dataset(test_sentences, test_tags)

print("Accuracy:")
print(clf.score(X_test, y_test))

