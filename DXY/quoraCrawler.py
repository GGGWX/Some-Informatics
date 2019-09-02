import urllib.request
import ssl
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from bs4 import BeautifulSoup
from lxml import etree
import re
import os
import time
import random
import threading
import csv
import nltk
import json



ssl._create_default_https_context = ssl._create_unverified_context
base = 'https://answers.search.yahoo.com/search;_ylt=AwrXnCCxbDdc3WwA80VPmolQ;_ylu=X3oDMTFhamFnNGFoBGNvbG8DZ3ExBHBvcwMxBHZ0aWQDQjI1NTlfMQRzZWMDcGFnaW5hdGlvbg--?p=quit+smoking&type=2button&fr=uh3_answers_vert_gs&fr2=sb-top-answers.search&'

subpart = 'b=1&pz=10&bct=0&xargs=0'

webaddress = 'https://www.quora.com/search?q=Quit+smoking'
abc = base + subpart





#Quora爬虫
def login(account, password):
    driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
    driver.get("https://www.quora.com/")
    time.sleep(2)
    driver.find_element_by_xpath("//input[@tabindex='1']").send_keys(account)
    time.sleep(2)
    driver.find_element_by_xpath("//input[@tabindex='2']").send_keys(password)
    time.sleep(100)
    driver.find_element_by_xpath("//input[@tabindex='4']").click()
    time.sleep(5)
    #获取问题的URL
    driver.get("https://www.quora.com/topic/Machine-Learning/all_questions")
    # driver.get("https://www.quora.com/search?q=machine+learning")
    cnt = 1
    #移动滚动条至底部
    while True:
        # 把滚动条拖到最下面
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)  # 等待5秒
        driver.implicitly_wait(5)  # 等待5秒

        cnt = cnt + 1
        print(cnt)
        if cnt >= 1000:
            break
    #移动完毕
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    urls = []
    Titles = soup.find_all('span', attrs={'class':'ui_qtext_rendered_qtext'})
    TimeStamps = soup.find_all('span', attrs={'class':'question_timestamp'})
    # Answers = soup.find_all('a', attrs={'class':'answer_count_prominent'})
    # Follows = soup.find_all('span', attrs={'class':'ui_button_count_inner'})
    Links = soup.find_all('a', attrs={'class':'question_link'})
    for link in Links:
        url = "https://www.quora.com" + link['href']
        urls.append(url)
    
    #移动完毕后，求出该页面所有回答数
    sum = 0
    for p in Titles:
        sum = sum + 1
    #写入csv    
    with open("result3.csv", "w", encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        # writer.writerow(["Question", "Timestamp", "AnswerCoutnt", "Follows", "URL"])
        writer.writerow(["Question", "URL", "Time"])
        counter = 0
        while True:
            writer.writerow([Titles[counter].get_text(), urls[counter], TimeStamps[counter].get_text()])
            # writer.writerow([Titles[counter].get_text(), TimeStamps[counter].get_text(), Answers[counter].get_text(), Follows[counter+1].get_text(), urls[counter]])
            counter = counter + 1
            print(counter)
            if counter >= sum:
                break




def getHtml(url):
    # user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:67.0) Gecko/20100101 Firefox/67.0'
    # header={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
    header = {  'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:67.0) Gecko/20100101 Firefox/67.0',
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'}
    req = urllib.request.Request(url, headers=header)
    html = urllib.request.urlopen(req).read().decode('utf8')
    return html
    # html = urllib.request.urlopen(url).read().decode('gbk')
    # return html

def getQuestion(html):
    
    targetwebsiteContent =  getHtml(html)
    print(targetwebsiteContent)


def main():
    getQuestion(webaddress)    
    user = "xxx"
    password = "xxx"
    login(user, password)
    #Zhihu()
    # str = ' '
    # words = "H ow do I convince someone to stop smoking weed?"
    # porter_stemmer = PorterStemmer()
    # nltk_tokens = nltk.word_tokenize(words)
    # processed_singleword = []
    # for w in nltk_tokens:
    #     processed_singleword.append(porter_stemmer.stem(w))
    # print(str.join(processed_singleword))

    # stoplist = stopwords.words('english')
    # text = "This is just a test!"
    # cleanword = [word for word in text.lower().split() if word not in stoplist]
    # print(cleanword)



if __name__ == '__main__':
    main()
