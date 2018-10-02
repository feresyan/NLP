def read_dataset(fname):
    sentences = []
    tags = []
    with open(fname) as f:
        content = f.readlines()
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
        sentences.append(sent)
        tags.append(tag)
        idx_line = idx_line+2 
    return sentences, tags       

 
sentences,tags = read_dataset('Data2.tsv')
print(sentences[0])
print(tags[0])

# Split the dataset for training and testing
training_sentences = sentences[:1000]
test_sentences = sentences[1000:1020]
training_tags = tags[:1000]
test_tags = tags[1000:1020]

training=[]

for i in range (len(training_sentences)):
    for j in range (len(training_sentences[i])):
        kata = (training_sentences[i][j],training_tags[i][j])
        training.append(kata)
# print(training)

import nltk
from collections import Counter
cntKata = Counter()
for i in range (len(training_sentences)):
    for j in range (len(training_sentences[i])):
        kata=training_sentences[i][j]
        if kata in cntKata :
            cntKata[kata]+=1
        else:
            cntKata[kata]=1
# for kata in training_sentences:
#     if kata in cntKata :
#         cntKata[kata]+=1
#     else:
#         cntKata[kata]=1

cntBasedLine={}

for kata in range (len(training)):
    if kata in cntBasedLine :
        cntBasedLine[kata]+=1
    else:
        cntBasedLine[kata]=1

# print (cntBasedLine['yang'])
# kataUji=input("Silahkan masukkan kata yang ingin di uji : ")
