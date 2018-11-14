import csv
import lxml
from lxml import etree
import requests

f = open("./NBA_2018_19_salary.csv", "w+")

basicURL = 'https://www.basketball-reference.com/contracts/players.html'

def get_html(str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36', }
    req = requests.get(url=str, headers=headers).text
    return req

fixed_path = '//*[@id="player-contracts"]/tbody/tr'

def get_info(url):
    selector = etree.HTML(get_html(url))

    try:
        writer = csv.writer(f)
        writer.writerow(('player', 'team', 'salary'))

        for i in range(535):
            player = selector.xpath(
                fixed_path + '[' + str(i) + ']/td[1]/a/text()')
            if not player:
                continue
            player = player[0]

            team = selector.xpath(
                fixed_path + '[' + str(i) + ']/td[2]/a/text()')
            if not team:
                continue
            team = team[0]

            salary = selector.xpath(
                fixed_path + '[' + str(i) + ']/td[3]/text()')
            if not salary:
                continue
            salary = salary[0][1:].replace(',', '')

            writer.writerow((player, team, salary))
    finally:
        f.close()

get_info(basicURL)
