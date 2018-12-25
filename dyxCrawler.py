#from requests_html import HTMLSession
import time
import re
import requests
import csv, codecs
import lxml
from lxml import etree
from lxml import html
import pymysql

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


def get_info(url):
    selector = etree.HTML(get_html(url))

    for i in range(1, 36):
        # title = selector.xpath(fixed_path + '[' + str(i) + ']/td[2]/a/text()')
        # if title:
        #     title = title[0]
        # else:
        #     continue
        # title = selector.xpath(fixed_path + '[' + str(i) + ']/td[2]/a/text()')
        # if not title:
        #     new_title = selector.xpath(fixed_path + '[' + str(i) + ']/td[2]/a[2]/text()')
        #     title = title[0]
        # else:
        #     title = title[0]
        title = selector.xpath(fixed_path + '[' + str(i) + ']/td[2]/a[last()]/text()')[0]
        print(title)
        # attr = selector.xpath(fixed_path + '[' +str(i) + ']/td[2]/a/@class/text()')
        # if attr:
        #     title = selector.xpath(fixed_path + '[' + str(i) + ']/td[2]/a[2]/text()')[0]
        # else:
        #     title = selector.xpath(fixed_path + '[' + str(i) + ']/td[2]/a/text()')[0]
        # //*[@id="col-1"]/table[3]/tbody/tr[25]/td[2]/a[1] 
        # //*[@id="col-1"]/table[3]/tbody/tr[25]/td[2]/a[2]
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

    first_floors = selector.xpath(' \
    //*[@id="post_1"]/table/tbody/tr/td[2]/div[2]/div[1]/table/tbody/tr/td//p/text() | \
    //*[@id="post_1"]/table/tbody/tr/td[2]/div[2]/div[1]/table/tbody/tr/td//p//a/text() | \
    //*[@id="post_1"]/table/tbody/tr/td[2]/div[2]/div[1]/table/tbody/tr/td//p//strong/text() | \
    //*[@id="post_1"]/table/tbody/tr/td[2]/div[2]/div[1]/table/tbody/tr/td//text() | \
    //*[@id="post_1"]/table/tbody/tr/td[2]/div[2]/div[2]/table/tbody/tr/td//text() ')
    first_floors2 = [str(i) for i in first_floors]
    first_floors3 = ''.join(first_floors2)
    # print(first_floors3)
    return first_floors3

#max_page = int(etree.HTML(testHTML).xpath('//*[@id="col-1"]/div/div[1]/div[1]/a[4]/text()')[0])
#max pages the bbs have

# //*[@id="post_1"]/table/tbody/tr/td[2]/div[2]/div[1]/table/tbody/tr/td
# //*[@id="post_1"]/table/tbody/tr/td[2]/div[2]/div[1]/table/tbody/tr/td/text()



if __name__ == "__main__":
    
    # j = 2 #first page
    # url = basicURL + '&tpg=' + str(j)
    # get_info(url)
    # print(urls[0])
    # j = 2
    # while(j <= 10):
    #     url = basicURL + '&tpg=' + str(j)
    #     get_info(url)
    #     j = j + 1
    # for n in range(122,124):
    #     url = basicURL + '&tpg=' + str(n)
    #     get_info(url)
    get_info("http://www.dxy.cn/bbs/board/106?order=1&tpg=177")
    

    




#//*[@id="col-1"]/div/div[1]/div[1]/a[4]        all pages
#//*[@id="col-1"]/table[3]/tbody/tr[1]          odd...
#//*[@id="col-1"]/table[3]/tbody/tr[2]          even...
#//*[@id="col-1"]/table[3]/tbody/tr[1]/td[2]/a  title
#//*[@id="col-1"]/table[3]/tbody/tr[1]/td[3]/a  author
#//*[@id="col-1"]/table[3]/tbody/tr[1]/td[3]/em when
#//*[@id="col-1"]/table[3]/tbody/tr[1]/td[4]/a  reply
#//*[@id="col-1"]/table[3]/tbody/tr[1]/td[4]/em click
#//*[@id="col-1"]/table[3]/tbody/tr[1]/td[5]/em lastReply