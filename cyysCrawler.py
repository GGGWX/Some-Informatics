import requests
import csv
import time
from lxml import etree

f = open("./cyys.csv", "w+", encoding = "utf-8-sig")
writer = csv.writer(f)
writer.writerow(('title', 'when', 'diagnosis'))

def get_html(str):
    headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36', }
    req = requests.get(url = str, headers = headers).text
    return req

def get_info(url):
    selector = etree.HTML(get_html(url))
    for i in range(1, 21):
        when = selector.xpath('/html/body/div[4]/div[2]/div[' + str(i) + ']/span/text()')[0]
        content_url = selector.xpath('/html/body/div[4]/div[2]/div[' + str(i) + ']/div[1]/a/@href')[0]
        post_url = 'https://www.chunyuyisheng.com' + content_url
        title, diagnonsis = get_content(post_url)
        writer.writerow((title, when, diagnonsis))

def get_content(url):
    selector = etree.HTML(get_html(url))
    title = selector.xpath('/html/body/div[5]/div[1]/span/text()')
    if not title:
        title = 'page not found'
    else:
        title = title[0]
    diagnosis = selector.xpath('/html/body/div[5]/div[2]/div[5]/p[2]/text()')
    if not diagnosis:
        diagnosis = '无'
    else:
        diagnosis = diagnosis[0]
    return title, diagnosis

if __name__ == "__main__":
    for n in range (19, 20):
        url = 'https://www.chunyuyisheng.com/pc/search/qalist/?query=%E6%88%92%E7%83%9F&page=' + str(n)
        get_info(url)
        time.sleep(1)
