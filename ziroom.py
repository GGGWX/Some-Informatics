import requests
from lxml import etree
from bs4 import BeautifulSoup
import re
import time
import urllib
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pytesseract
import random
import csv

options = Options()
options.add_argument('blink-settings=imagesEnabled=false')
options.add_argument('--headless')

browser = webdriver.Chrome(chrome_options=options)

f = open("ziroom.csv", "w+", encoding="utf-8-sig")
writer = csv.writer(f)
writer.writerow(('url', 'price'))

def get_image(html):
    photo = re.findall('var ROOM_PRICE = {"image":"(//.*?.png)"', html)[0]
    image = requests.get('http:' + photo).content
    f = open('price.png', 'wb')
    f.write(image)
    f.close()
    num = []
    number = pytesseract.image_to_string(Image.open("price.png"), config="--psm 8 -c tessedit_char_whitelist=1234567890")
    for i in number:
        num.append(i)
    return num

def get_html(html, page):
    # headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
    url = html + '?p=' + str(page)
    # req = requests.get(url = url,headers = headers).text
    # return req
    browser.get(url)
    time.sleep(random.randint(0, 3))
    response = browser.page_source
    return response

def get_info(html, num_list):
    data = etree.HTML(html)
    items = data.xpath('//*[@id="houseList"]/li[@class="clearfix"]')
    for item in items:
        temp_list = []
        price_list = []

        title = item.xpath('./div[2]/h3/a/@href')[0]
        #//*[@id="houseList"]/li[2]/div[2]/h3/a
        #//*[@id="houseList"]/li[2]/div[1]/a
        # print(title)
        post_url = 'http:' + str(title)
        # print(post_url)
        prices = item.xpath('./div[3]/p[1]/span[position()>1]/@style')
        # print(prices)
        for price in prices:
            temp_list.append(price.replace("background-position:-", "").replace("px", ""))
        # print(temp_list)
        for number in temp_list:
            price = num_list[int(int(number) / 30)]
            # print(price)
            # dont know why tesseract cannot judge number 7
            if price == '/':
                price = '7'
            if price =='(':
                price = '7'
            price_list.append(price)
        # print(temp_list)
        price_final = ''.join(price_list)
        # print(price_final)
        # print('-'*20)
        writer.writerow((post_url, price_final))

if __name__ == "__main__":
    # time.sleep(1)
    print('')
    url = 'http://www.ziroom.com/z/nl/z1.html'
    for i in range (1, 51):
        print("正在爬取第" + str(i) + "页")
        html = get_html(url, i)
        # print(html)
        num_list = get_image(html)
        # print(num_list)
        get_info(html, num_list)

        
