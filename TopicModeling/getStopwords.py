import sys
eng_stopwords = []
with open('eng_stopwords.txt', 'r') as f:
    for line in f:
        eng_stopwords.append(line.strip('\n').split(',')[0])

print(eng_stopwords)