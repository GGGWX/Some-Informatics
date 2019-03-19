def topicAnalyze(self):
    from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
    from sklearn.decomposition import NMF, LatentDirichletAllocation
    import random
    from time import time
    import pandas as pd
    screen_names,texts = self.get_all_texts() ####获取所有文本

    bow_corpus = []
    for trace in texts:
        bow_corpus.append(trace)
    train_size = int(round(len(bow_corpus)*0.8))###分解训练集和测试集
    train_index = sorted(random.sample(range(len(bow_corpus)), train_size))###随机选取下标
    test_index = sorted(set(range(len(bow_corpus)))-set(train_index))
    train_corpus = [bow_corpus[i] for i in train_index]
    test_corpus = [bow_corpus[j] for j in test_index]

    n_features = 2000
    n_top_words = 1000

    print("Extracting tf features for LDA...")
    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2,max_features=n_features,stop_words='english')###选取至少出现过两次并且数量为前2000的单词用来生成文本表示向量
    t0 = time()
    tf = tf_vectorizer.fit_transform(train_corpus)###使用向量生成器转化测试集
    print("done in %0.3fs." % (time() - t0))
    # Use tf (raw term count) features for LDA.
    print("Extracting tf features for LDA...")
    tf_test = tf_vectorizer.transform(test_corpus)
    print("done in %0.3fs." % (time() - t0))
    grid = dict()
    t0 = time()
    for i in range(1,100,2): ###100个主题，以5为间隔
        grid[i] = list()
        n_topics = i

        lda = LatentDirichletAllocation(n_components=n_topics, max_iter=5,learning_method='online',learning_offset=50.,random_state=0) ###定义lda模型
        lda.fit(tf) ###训练参数
        train_gamma = lda.transform(tf) ##得到topic-document 分布
        train_perplexity = lda.perplexity(tf)
        test_perplexity = lda.perplexity(tf_test) ###s计算测试集困惑度
        print('sklearn preplexity: train=%.3f' %(train_perplexity))

        grid[i].append(train_perplexity)

    print("done in %0.3fs." % (time() - t0))

    df = pd.DataFrame(grid)
    df.to_csv('cn.csv')
    print(df)
    plt.figure(figsize=(14,8), dpi=120)
    #plt.subplot(221)
    plt.plot(df.columns.values, df.iloc[0].values, '#007A99')
    plt.xticks(df.columns.values)
    plt.ylabel('train Perplexity')
    plt.show()
    plt.savefig('lda_topic_perplexity.png', bbox_inches='tight', pad_inches=0.1)

if __name__ == "__main__":
    topicAnalyze()