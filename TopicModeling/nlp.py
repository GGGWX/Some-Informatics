import pandas as pd
import jieba.posseg as psg
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation

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

fo = open("new_cuttedwords.txt", "w+")
for row in df.content:
    fo.writelines(preprocess(row)+"\n")
fo.close()



# n_features = 2000
# n_topics = 3
# n_top_words = 20

# #向量化
# tf_vectorizer = CountVectorizer(strip_accents='unicode',
#                                 max_features=n_features,
#                                 max_df=0.95,
#                                 min_df=10)
# tf = tf_vectorizer.fit_transform(df.cutted_words)

# #训练参数
# lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=50,
#                                 learning_method='online',
#                                 learning_offset=50.,
#                                 random_state=0)
# lda.fit(tf)

# #显示话题
# def print_top_words(model, feature_names, n_top_words):
#     for topic_idx, topic in enumerate(model.components_):
#         print("Topic %d:" % topic_idx)
#         print(" ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]))
#     print()


# tf_feature_names = tf_vectorizer.get_feature_names()
# print_top_words(lda, tf_feature_names, n_top_words)