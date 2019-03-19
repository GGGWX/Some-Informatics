import jieba.analyse
from string import digits

with open('new_quora_cut.txt') as f:
    lines = f.readlines()


sentences = []
for line in lines:
    sentence = ''.join(line.strip())
    sentences.append(sentence)

# print(sentences)
topics = []
f = open('quora_result.txt', 'w+')
for sentence in sentences:
    topic = jieba.analyse.extract_tags(sentence, topK=5, withWeight=True, allowPOS=())
    topics.append(topic)
print(len(topics))
for i in topics:
    if i == []:
        pass
    for tup in i:
        f.write(tup[0] + ' ')
    f.write("\r\n")
    
f.close()

    # for item in topic:
        # print(item[0], item[1])
        
        # print(item[0])
    # topics.append(topic)

