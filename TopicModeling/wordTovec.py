# from gensim.models import word2vec
from sklearn.decomposition import PCA
import word2vec
import pandas as pd
import numpy as np
import jieba.posseg as psg
import logging
import os

stopwords = [line.strip() for line in open('stopwords.txt').readlines()]
stopwords += [line.strip() for line in open('stopwords2.txt', encoding="gbk").readlines()]
stopwords += [line.strip() for line in open('stopwords3.txt', encoding="gbk").readlines()]


def filter(flag):
    return not (flag.startswith('d') or flag.startswith('p') or 
                flag.startswith('u') or flag.startswith('c') or 
                flag.startswith('q') or flag.startswith('e') or 
                flag.startswith('h') or flag.startswith('k') or 
                flag.startswith('ds') or flag.startswith('m') or
                flag.startswith('mq') or flag.startswith('ry') or
                flag.startswith('t') or flag.startswith('tg') or
                flag.startswith('vyou'))


def preprocess(text):
    result = ""
    words = [x.word for x in psg.cut(text.strip()) if filter(x.flag)]
    for word in words:
        if word not in stopwords:
            if word != '\r\n':
                result += word
                result += " "
    return result

df = pd.read_csv("cn.csv")
df["cutted_words"] = df.content.apply(preprocess)
print("cut finished")

fo = open("cuttedwords.txt", "w+")
for row in df.content:
    fo.write(preprocess(row))
fo.close()

# def model_train(train_file_name, save_model_file):  # model_file_name为训练语料的路径,save_model为保存模型名
#     print ('model_train begin.')
#     try:
#         # 模型训练，生成词向量
#         logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
#         sentences = word2vec.Text8Corpus(train_file_name)  # 加载语料
#         model = word2vec.Word2Vec(sentences, size=2500, min_count=10, sg=1)  # 训练skip-gram模型; 默认window=5
#         model.save(save_model_file)
#         model.wv.save_word2vec_format(save_model_file + ".bin", binary=True)   # 以二进制类型保存模型以便重用
#     except BaseException as e:  # 因BaseException是所有错误的基类，用它可以获得所有错误类型
#         print(Exception, ":", e)    # 追踪错误详细信息
#     print ('model_train end.')

train_file_name = "cuttedwords.txt"
save_model_file = "cuttedwords.model"

# model_train(train_file_name, save_model_file)

model_file = "cuttedwords.model"
model_file_bin = "cuttedwords.model.bin"

word2vec.word2vec('cuttedwords.txt', 'cnword2vec.bin', size=2500, verbose=True)


def word2vec_test():
    print ('word2vec_test begin.')
    try:
        # 加载日志输出配置
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

        # 训练模型
        print ('从文件:%s 训练模型存放在: %s' % (train_file_name, model_file))
        # if not os.path.exists(model_file):     # 判断文件是否存在
        #     model_train(train_file_name, model_file)
        # else:
        #     print('此训练模型已经存在，不用再次训练')
        model_train(train_file_name, model_file)

        # 加载已训练好的模型
        print ('从文件:%s 中加载模型' % model_file)
        # model_1 = gensim.models.KeyedVectors.load_word2vec_format(model_file_bin, binary=True)
        model_1 = word2vec.Word2Vec.load(model_file)

        # 计算某个词的相关词列表
        y2 = model_1.most_similar(u"吸烟", topn=19)  # 39个最相关的
        print(u"和吸烟最相关的词有:\n")
        for item in y2:
            print ("%s: %g" % (item[0], item[1]))
        print("-------------------------------\n")
    except Exception:
        print ("Exception")
    print ('word2vec_test end.')

# word2vec_test()


model = word2vec.load('cnword2vec.bin')


word2vec.word2clusters('cuttedwords.txt','cncluster.txt', 100, verbose=True)
clusters = word2vec.load_clusters('cncluster.txt')
print(clusters)
# clusters.vocab
# print(clusters.get_words_on_cluster(90)[:10])

# model.clusters = clusters
# indexes, metrics = model.analogy(pos=["吸","戒烟"], neg=["抽"])
# print(model.generate_response(indexes, metrics).tolist())



