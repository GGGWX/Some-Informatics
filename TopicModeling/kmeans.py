import pandas as pd
import jieba.posseg as psg
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.metrics import calinski_harabaz_score
import matplotlib.pyplot as plt
import numpy as np

stopwords = [line.strip() for line in open('stopwords.txt').readlines()]
stopwords += [line.strip() for line in open('stopwords2.txt', encoding="gbk").readlines()]
stopwords += [line.strip() for line in open('stopwords3.txt', encoding="gbk").readlines()]


def filter(flag):
    return not (flag.startswith('d') or flag.startswith('p') or 
                flag.startswith('u') or flag.startswith('c') or 
                flag.startswith('q') or flag.startswith('e') or 
                flag.startswith('h') or flag.startswith('k') or 
                flag.startswith('ds') or flag.startswith('m') or
                flag.startswith('mq') or flag.startswith('ry'))


def preprocess(text):
    result = ""
    words = [x.word for x in psg.cut(text.strip()) if filter(x.flag)]
    for word in words:
        if word not in stopwords:
            if word != '\r\n':
                result += word
                result += " "
    return result


# 文本分词 去停用词
df = pd.read_csv("cn.csv")
df["cutted_words"] = df.content.apply(preprocess)
print("cut finish")

#向量化
tf_vectorizer = CountVectorizer(strip_accents='unicode',
                                max_features=2000,
                                max_df=0.95,
                                min_df=10)
tf = tf_vectorizer.fit_transform(df.cutted_words)

SSE = []
sc_scores = []
calniski_scores = []
clusters = range(1,10)
for k in clusters:
    estimator = KMeans(n_clusters=k).fit(tf)
    SSE.append(estimator.inertia_)
    
    # sc_score = silhouette_score(tf, estimator.labels_, metric="euclidean")
    # sc_scores.append(sc_score)
    # plt.title('K = %s, silhouette coef = %0.03f'%(k, sc_score))

    # calinski_score = calinski_harabaz_score(tf.todense(), estimator.labels_)
    # calniski_scores.append(calinski_score)
    # plt.title('K = %s, calniski index = %0.03f'%(k, calinski_score))

# plt.figure()
# plt.plot(clusters, sc_scores, '*-')
# plt.show()        
# plt.figure()
# plt.plot(clusters, calniski_scores, '*-')
# plt.show()

X = range(1,10)
plt.xlabel('k')
plt.ylabel('SSE')
plt.margins(x=0,y=-0.05)
plt.plot(X, SSE, 'o-')
plt.show()
