import time
import requests
import csv, codecs
import lxml
from lxml import etree

f = open("../dxyhl.csv", "w+", encoding="utf-8-sig")

basicURL = 'http://www.dxy.cn/bbs/board/106?order=1'

def get_html(str):
    headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36', }
    req = requests.get(url = str, headers = headers).text
    return req

fixed_path = '//*[@id="col-1"]/table[3]/tbody/tr'

urls=[]   

writer = csv.writer(f)
writer.writerow(('title', 'author', 'when', 'reply', 'click', 'rate', 'content'))

# know nothing about python crawler, but chrome is a good tool to analyze xml
# and fortunately i learned xml, so use xml to write a crawler
# (regex looks like disaster). I have to say dxy is a website with weird structure
# spend much time on it, finally it worked fine. I hope that if someday i become a
# front-end programmer, the structure must be limpid for others to read.

def get_info(url):
    selector = etree.HTML(get_html(url))
# maybe there should exist a try-catch block, i dismiss it
    for i in range(1, 36):
        title = selector.xpath(fixed_path + '[' + str(i) + ']/td[2]/a[last()]/text()')[0]
        # print(title) 
        author = selector.xpath(fixed_path + '[' + str(i) + ']/td[3]/a/text()')[0]
        # print(author)
        when = selector.xpath(fixed_path + '[' + str(i) + ']/td[3]/em/text()')[0]
        # print(when)
        reply = int(selector.xpath(fixed_path + '[' + str(i) + ']/td[4]/a/text()')[0])
        # print(reply)
        click = int(selector.xpath(fixed_path + '[' + str(i) + ']/td[4]/em/text()')[0])
        # print(click)
        reply_rate = reply/click
        rate = round(reply_rate, 8) #取8位有效数字 个人感觉精确度已经够了
        # print(rate)
        post_url = selector.xpath(fixed_path + '[' + str(i) + ']/td[2]/a[last()]/@href')[0]
        # print(post_url)
        urls.append(post_url)
        content = get_content(post_url)
        writer.writerow((title, author, when, reply, click, rate, content))


def get_content(url):
    selector = etree.HTML(get_html(url))
# this part may be optimized, and most of the posts have no reply, so only grab the main floor
    first_floors = selector.xpath(' \
    //*[@id="post_1"]/table/tbody/tr/td[2]/div[2]/div[1]/table/tbody/tr/td//p/text() | \
    //*[@id="post_1"]/table/tbody/tr/td[2]/div[2]/div[1]/table/tbody/tr/td//p//a/text() | \
    //*[@id="post_1"]/table/tbody/tr/td[2]/div[2]/div[1]/table/tbody/tr/td//p//strong/text() | \
    //*[@id="post_1"]/table/tbody/tr/td[2]/div[2]/div[1]/table/tbody/tr/td//text() | \
    //*[@id="post_1"]/table/tbody/tr/td[2]/div[2]/div[2]/table/tbody/tr/td//text() ')
    first_floors2 = [str(i) for i in first_floors]
    first_floor = ''.join(first_floors2)
    # print(first_floor)
    return first_floor

max_page = int(etree.HTML(testHTML).xpath('//*[@id="col-1"]/div/div[1]/div[1]/a[4]/text()')[0])
#max pages the bbs have

if __name__ == "__main__":
    for n in range(1, max_page + 1):
        url = basicURL + '&tpg=' + str(n)
        get_info(url)
        time.sleep(1)# whatever, connot afford a proxy ip
