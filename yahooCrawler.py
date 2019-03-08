import time
import requests
import csv
import numpy as np
import random
from lxml import etree

f = open("../yahoo_answers_stop_smoking.csv", "a+", encoding="utf-8-sig")
writer = csv.writer(f)
writer.writerow(('title', 'when', 'reply', 'description'))

def get_html(str):
    headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
    req = requests.get(url = str,headers = headers).text
    return req

def get_info(url):
    selector = etree.HTML(get_html(url))
    for i in range (1, 11):
        title_a = selector.xpath('//*[@id="web"]/ol[2]/li[' + str(i) + ']/div/div[1]/h3//text()')
        titles = [str(n) for n in title_a]
        title = ''.join(titles)
        when = selector.xpath('//*[@id="web"]/ol[2]/li[' + str(i) + ']/div/div[3]/p/span[2]/text()')[0].replace(' · ', '')
        reply = selector.xpath('//*[@id="web"]/ol[2]/li[' + str(i) + ']/div/div[3]/p/span[1]/text()')[0].replace(' Answers ·', '')
        url = selector.xpath('//*[@id="web"]/ol[2]/li[' + str(i) + ']/div/div[1]/h3/a/@href')[0]
        description = get_content(url)
        time.sleep(2)
        writer.writerow((title, when, reply, description))

def get_content(url):
    selector = etree.HTML(get_html(url))
    description = selector.xpath('//*[@class="Mstart-75 Mr-14 Pos-r"]/div[last()-2]/span[last()]/text()')
    if not description:
        description = 'none'
    else:
        description = description[0]
    return description

if __name__ == "__main__":
    number_list = list(set(np.random.randint(0, 101, size=1500).tolist()))
    random.shuffle(number_list)
    # print(number_list)
    # print(len(number_list))
    while len(number_list):
        n = number_list.pop() * 10 + 1
        print(n)
        get_info('https://answers.search.yahoo.com/search;_ylt=AwrXgSOqmVFcWX4A9XRPmolQ;_ylu=X3oDMTFhOWY4YTJzBGNvbG8DZ3ExBHBvcwMxBHZ0aWQDQjI1NTdfMQRzZWMDcGFnaW5hdGlvbg--?p=stop+smoking&pz=10&type=2button&fr=uh3_answers_vert_gs&fr2=sb-top-answers.search&bct=0&b=' + str(n) + '&pz=10&bct=0&xargs=0')
        time.sleep(5)
