import pandas as pd
import jieba.posseg as psg
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import calinski_harabaz_score
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import numpy as np
from nltk.tokenize import WordPunctTokenizer
import json

stopwords = [line.strip() for line in open('eng_stopwords.txt').readlines()]

def preprocess(text):
    result = ""
    words = WordPunctTokenizer().tokenize(text)
    for word in words:
        if word not in stopwords:
            if word != "\r\n":
                result += word
                result += " "
    return result

#文本分词 去停用词
df = pd.read_csv("quora_completed.csv")
df["cutted_words"] = df.content.apply(preprocess)


tf_vectorizer = CountVectorizer(strip_accents='unicode',
                                max_features=2000,
                                max_df=0.95,
                                min_df=10)
tf = tf_vectorizer.fit_transform(df.cutted_words)

# tfidf = TfidfTransformer().fit_transform(tf.toarray())
# print(tfidf)
# print(tf_vectorizer.vocabulary_)


# engwords = tf_vectorizer.vocabulary_
# engwords = sorted(engwords.items(), key = lambda x:x[1], reverse=True)
# print(engwords)
clusters = range(2,10)
calniski_scores = []
sc_scores = []
def getK():
    SSE = []
    for k in clusters:
        estimator = KMeans(n_clusters=k)
        estimator.fit(tf)
        SSE.append(estimator.inertia_)
        sc_score = silhouette_score(tf, estimator.labels_, metric="euclidean")
        sc_scores.append(sc_score)
        plt.title('K = %s, silhouette coef = %0.03f'%(k, sc_score))
        # calinski_score = calinski_harabaz_score(tf.todense(), estimator.labels_)
        # calniski_scores.append(calinski_score)
        # plt.title('K = %s, calniski index = %0.03f'%(k, calinski_score))

# X = range(1,10)
# plt.xlabel('k')
# plt.ylabel('SSE')
# plt.plot(X, SSE, 'o-')
# plt.show()

getK()
# plt.figure()
# plt.plot(clusters, calniski_scores, '*-')
# plt.show()
plt.figure()
plt.plot(clusters, sc_scores, '*-')
plt.show()  