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

dest = 'http://www.keai99.com/forum.php?mod=forumdisplay&fid=36&filter=lastpost&orderby=lastpost'

f = open("./keaicomp.csv", "a", encoding="utf-8-sig")
writer = csv.writer(f)
writer.writerow(["title", "link", "posttime", "click", "reply", "author"])

def get_html(str):
    headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36', }
    req = requests.get(url = str, headers = headers).text
    return req

# //*[@id="threadlisttableid"]
# //*[@id="normalthread_460632"]/tr/th/a[3]
# /html/body/div[7]/div[5]/div/div/div[4]/div[2]/form/table/tbody[2]/tr/th/a[3]
# /html/body/div[7]/div[5]/div/div/div[4]/div[2]/form/table/tbody[31]/tr/th/a[2]
# /html/body/div[7]/div[5]/div/div/div[4]/div[2]/form/table/tbody[32]/tr/th/a[3]
# /html/body/div[7]/div[5]/div/div/div[4]/div[2]/form/table/tbody[2]/tr/th/a[3]


def get_info(url):
    selector = etree.HTML(get_html(url))
    for i in range(32,38):
        title = selector.xpath('//*[@id="threadlisttableid"]/tbody[' + str(i) + ']/tr/th/a[3]/text()')[0]

        link = selector.xpath('//*[@id="threadlisttableid"]/tbody[' + str(i) + ']/tr/td[1]/a/@href')[0]

        posttime = selector.xpath('//*[@id="threadlisttableid"]/tbody[' + str(i) + ']/tr/td[2]/em/span/text()')[0]
        time = posttime[:-6]

        reply = selector.xpath('//*[@id="threadlisttableid"]/tbody[' + str(i) + ']/tr/td[3]/a/text()')[0]

        click = selector.xpath('//*[@id="threadlisttableid"]/tbody[' + str(i) + ']/tr/td[3]/em/text()')[0]

        author = selector.xpath('//*[@id="threadlisttableid"]/tbody[' + str(i) + ']/tr/td[2]/cite/a/text()')[0]

        writer.writerow((title, link, time, click, reply, author))



def login(account, password):
    driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')

    driver.get("http://keai99.com/")
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="ls_username"]').send_keys(account)
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="ls_password"]').send_keys(password)
    time.sleep(10)
    driver.find_element_by_xpath('//*[@id="lsform"]/div/div[1]/table/tbody/tr[2]/td[3]/button').click()
    time.sleep(5)

    driver.get("http://www.keai99.com/forum.php?mod=forumdisplay&fid=36&orderby=lastpost&orderby=lastpost&filter=lastpost&page=95")

    time.sleep(1)
    # 94面没爬完


    count = 95

    while count <= 226:

        selector = etree.HTML(get_html(driver.current_url))
        for i in range(6,38):
            title = selector.xpath('//*[@id="threadlisttableid"]/tbody[' + str(i) + ']/tr/th/a[3]/text()')[0]

            link = selector.xpath('//*[@id="threadlisttableid"]/tbody[' + str(i) + ']/tr/td[1]/a/@href')[0]

            posttime = selector.xpath('//*[@id="threadlisttableid"]/tbody[' + str(i) + ']/tr/td[2]/em/span/text()')[0]
            ptime = posttime[:-6]

            reply = selector.xpath('//*[@id="threadlisttableid"]/tbody[' + str(i) + ']/tr/td[3]/a/text()')[0]

            click = selector.xpath('//*[@id="threadlisttableid"]/tbody[' + str(i) + ']/tr/td[3]/em/text()')[0]

            author = selector.xpath('//*[@id="threadlisttableid"]/tbody[' + str(i) + ']/tr/td[2]/cite/a/text()')[0]

            writer.writerow((title, link, ptime, click, reply, author))

        driver.find_element_by_class_name('nxt').click()
        count = count + 1

if __name__ == "__main__":
    user = '252895817@qq.com'
    password = 'wsmzdwy61'
    # login(user, password)
    testurl = 'http://www.keai99.com/forum.php?mod=forumdisplay&fid=36&orderby=lastpost&orderby=lastpost&filter=lastpost&page=94'
    get_info(testurl)



