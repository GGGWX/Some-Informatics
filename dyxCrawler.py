import time
import requests
import csv, codecs
import lxml
from lxml import etree

f = open("../dxyhl.csv", "w+", encoding="utf-8-sig")
writer = csv.writer(f)
writer.writerow(('title', 'author', 'when', 'reply', 'click', 'rate', 'content'))

basicURL = 'http://www.dxy.cn/bbs/board/106?order=1'

# know nothing about python crawler, but chrome is a good tool to analyze xml
# and fortunately i learned xml, so use xml to write a crawler
# (regex looks like disaster). I have to say dxy is a website with weird structure
# spend much time on it, finally it worked fine. I hope that if someday i become a
# front-end programmer, the structure must be limpid for others to read.

def get_html(str):
    headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36', }
    req = requests.get(url = str, headers = headers).text
    return req

def get_info(url):
    selector = etree.HTML(get_html(url))
# maybe there should exist a try-catch block, i dismiss it
    for i in range(1, 36):
        title_span = selector.xpath('//*[@id="col-1"]/table[3]/tbody/tr[' + str(i) + ']/td[2]/a[last()]/span/text()')
        title_span_span = selector.xpath('//*[@id="col-1"]/table[3]/tbody/tr[' + str(i) + ']/td[2]/a[2]/span/span/text()')
        title_a = selector.xpath('//*[@id="col-1"]/table[3]/tbody/tr[' + str(i) + ']/td[2]/a[last()]/text()')
        if not title_span:
            if not title_span_span:
                title = title_a[0]
            else:
                title = title_span_span[0]
        else:
            title = title_span[0]
        author = selector.xpath('//*[@id="col-1"]/table[3]/tbody/tr[' + str(i) + ']/td[3]/a/text()')[0]
        when = selector.xpath('//*[@id="col-1"]/table[3]/tbody/tr[' + str(i) + ']/td[3]/em/text()')[0]
        reply = int(selector.xpath('//*[@id="col-1"]/table[3]/tbody/tr[' + str(i) + ']/td[4]/a/text()')[0])
        click = int(selector.xpath('//*[@id="col-1"]/table[3]/tbody/tr[' + str(i) + ']/td[4]/em/text()')[0])
        reply_rate = reply/click
        rate = round(reply_rate, 8) #取8位有效数字 个人感觉精确度已经够了
        post_url = selector.xpath('//*[@id="col-1"]/table[3]/tbody/tr[' + str(i) + ']/td[2]/a[last()]/@href')[0]
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
    return first_floor

#max_page = int(etree.HTML(basicURL).xpath('//*[@id="col-1"]/div/div[1]/div[1]/a[4]/text()')[0])
#max pages the bbs have

if __name__ == "__main__":
    for n in range(1, 10):
        url = basicURL + '&tpg=' + str(n)
        get_info(url)
        time.sleep(1)# whatever, connot afford a proxy ip
