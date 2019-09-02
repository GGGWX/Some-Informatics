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
import requests

dest = 'https://www.yinling.com.cn/forum.php?mod=forumdisplay&fid=46&filter=lastpost&orderby=lastpost'

f = open("./yinling.csv", "a", encoding="utf-8-sig")
writer = csv.writer(f)
writer.writerow(["title", "link", "posttime", "click", "reply", "author"])

def get_html(str):
    headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36', }
    req = requests.get(url = str, headers = headers).text
    return req

links = []

def get_info(url):
    selector = etree.HTML(get_html(url))
    for i in range(12,32):
        title = selector.xpath('//*[@id="threadlisttableid"]/tbody[' + str(i) + ']/tr/th/a[2]/text()')[0]

        link = selector.xpath('//*[@id="threadlisttableid"]/tbody[' + str(i) + ']/tr/td[1]/a/@href')[0]

        posttime = selector.xpath('//*[@id="threadlisttableid"]/tbody[' + str(i) + ']/tr/td[2]/em/span/text()')[0]

        reply = selector.xpath('//*[@id="threadlisttableid"]/tbody[' + str(i) + ']/tr/td[3]/a/text()')[0]

        click = selector.xpath('//*[@id="threadlisttableid"]/tbody[' + str(i) + ']/tr/td[3]/em/text()')[0]

        author = selector.xpath('//*[@id="threadlisttableid"]/tbody[' + str(i) + ']/tr/td[2]/cite/a/text()')[0]

        writer.writerow((title, link, posttime, click, reply, author))
    # 这个是第一面
    # 对于后面的


def login(account, password):
    driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')

    driver.get("https://www.yinling.com.cn/")
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="ls_username"]').send_keys(account)
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="ls_password"]').send_keys(password)
    time.sleep(10)
    driver.find_element_by_xpath('//*[@id="lsform"]/div/div[1]/table/tbody/tr[2]/td[3]/button').click()
    time.sleep(5)

    page = 2

    while page < 222:
        driver.get('https://www.yinling.com.cn/forum.php?mod=forumdisplay&fid=46&orderby=lastpost&orderby=lastpost&filter=lastpost&page=' + str(page))

        selector = etree.HTML(get_html(driver.current_url))

        for i in range(2,32):
            title = selector.xpath('//*[@id="threadlisttableid"]/tbody[' + str(i) + ']/tr/th/a[2]/text()')[0]

            link = selector.xpath('//*[@id="threadlisttableid"]/tbody[' + str(i) + ']/tr/td[1]/a/@href')[0]

            posttime = selector.xpath('//*[@id="threadlisttableid"]/tbody[' + str(i) + ']/tr/td[2]/em/span/text()')[0]

            reply = selector.xpath('//*[@id="threadlisttableid"]/tbody[' + str(i) + ']/tr/td[3]/a/text()')[0]

            click = selector.xpath('//*[@id="threadlisttableid"]/tbody[' + str(i) + ']/tr/td[3]/em/text()')[0]

            author = selector.xpath('//*[@id="threadlisttableid"]/tbody[' + str(i) + ']/tr/td[2]/cite/a/text()')[0]

            writer.writerow((title, link, posttime, click, reply, author))

            time.sleep(1)

        print('finish page:' + str(page))

        page = page + 1
        
if __name__ == "__main__":
    user = 'xxx'
    password = 'xxx'
    # login(user, password)
    get_info(dest)

