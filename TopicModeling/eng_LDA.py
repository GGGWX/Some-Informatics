import pandas as pd
import random
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from nltk.tokenize import WordPunctTokenizer
import matplotlib.pyplot as plt

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

# quora = pd.read_csv("./quora.csv")
# raw = []
# for line in quora:
#     line.strip(' ')


#区分训练集与测试集
bow_corpus = []
for content in df.cutted_words:
    bow_corpus.append(content)
train_size = int(round(len(bow_corpus)*0.8))###分解训练集和测试集
train_index = sorted(random.sample(range(len(bow_corpus)), train_size))###随机选取下标
test_index = sorted(set(range(len(bow_corpus)))-set(train_index))
train_corpus = [bow_corpus[i] for i in train_index]
test_corpus = [bow_corpus[j] for j in test_index]

n_features = 2000
                                        
#文本的向量化
tf_vectorizer = CountVectorizer(max_df=0.95, min_df=10,max_features=n_features)###选取至少出现过两次并且数量为前2000的单词用来生成文本表示向量
tf = tf_vectorizer.fit_transform(train_corpus)###使用向量生成器转化测试集
tf_test = tf_vectorizer.transform(test_corpus)
tf_all = tf_vectorizer.fit_transform(bow_corpus)

#确认主题数
grid = dict()
for i in range(1,20,1): ###100个主题，以5为间隔
    grid[i] = list()
    n_topics = i
    lda = LatentDirichletAllocation(n_components=n_topics, max_iter=5,learning_method='online',learning_offset=50.,random_state=0) ###定义lda模型
    lda.fit(tf_all) ###训练参数
    train_gamma = lda.transform(tf_all) ##得到topic-document 分布
    train_perplexity = lda.perplexity(tf_all)
    #test_perplexity = lda.perplexity(tf_test) ###s计算测试集困惑度
    print('sklearn preplexity for %d topics: train=%.3f' %(i, train_perplexity))
    grid[i].append(train_perplexity)


df = pd.DataFrame(grid)
df.to_csv('sklearn_perplexity.csv')
print(df)
plt.figure(figsize=(4,3), dpi=120)
#plt.subplot(221)
plt.plot(df.columns.values, df.iloc[0].values, '#007A99')
plt.xticks(df.columns.values)
plt.ylabel('train Perplexity')
plt.show()
plt.savefig('lda_topic_perplexity.png', bbox_inches='tight', pad_inches=0.1)