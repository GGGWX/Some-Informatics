from collections import Counter
import jieba.analyse
import re
import time

#分词模板
def cut_word(datapath):
    with open(datapath, 'r',encoding='utf-8') as fr:
        string=fr.read()
        print(type(string))
        #对文件中的非法字符进行过滤
        data=re.sub(r"[\s+\.\!\/_,$%^*(【】：\]\[\-:;+\"\']+|[+——！，。？、~@#￥%……&*（）]+|[0-9]+","",string)
        word_list= jieba.cut(data)
        print(word_list)
        return word_list
#词频统计模块
def statistic_top_word(word_list,top=100):
    #统计每个单词出现的次数，别将结果转化为键值对（即字典）
    result= dict(Counter(word_list))
    print(result)
    #sorted对可迭代对象进行排序
    #items()方法将字典的元素转化为了元组，而这里key参数对应的lambda表达式的意思则是选取元组中的第二个元素作为比较参数
    #排序厚的结果是一个列表，列表中的每个元素是一个将原字典中的键值对转化为的元祖
    sortlist=sorted(result.items(),key=lambda item:item[1],reverse=True)
    resultlist=[]
    for i in range(0,top):
        resultlist.append(sortlist[i])
    return resultlist

#主函数
def main():
    #设置数据集地址
    datapath='/Users/gggwx/Desktop/Some-Informatics/TopicModeling/test.csv'
    #对文本进行分词
    word_list=cut_word(datapath)
    #统计文本中的词频
    statistic_result=statistic_top_word(word_list,100)
    #输出统计结果
    print(statistic_result)

if __name__ == "__main__":
    main()
