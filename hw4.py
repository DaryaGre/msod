import requests
import datetime
from pprint import pprint
from pymongo import MongoClient
from lxml import html

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

client = MongoClient('127.0.0.1', 27017)

db = client['newss']

# яндекс
url = 'https://yandex.ru/news/'

response = requests.get(url, headers=header)
dom = html.fromstring(response.text)

items = dom.xpath("//div[contains(@class,'news-top-stories')]/div[contains(@class,'mg-grid__col')]")

ya_newss = []
for item in items:
    ya_news = {}
    name = item.xpath(".//a/h2/text()")
    link = item.xpath(".//span/a/@href")
    source = item.xpath(".//span/a/text()")
    time = item.xpath(".//span[@class='mg-card-source__time']/text()")

    ya_news['name'] = name[0]
    ya_news['link'] = link[0]
    ya_news['source'] = source[0]
    ya_news[
        'date'] = f'{str(datetime.datetime.now().day)}.{str(datetime.datetime.now().month)}.{str(datetime.datetime.now().year)} {time[0]}'

    ya_newss.append(ya_news)

yandex = db.yandex

yandex.insert_many(ya_newss)

for news in yandex.find({}):
    pprint(news)

# lenta

url = 'https://lenta.ru/'

response = requests.get(url, headers=header)
dom = html.fromstring(response.text)

items = dom.xpath("//section[contains(@class,'for-main')]//div[contains(@class,'item')]")

le_newss = []
for item in items:
    le_news = {}

    name = item.xpath(".//a[not(contains(@class,'topic-title-pic'))]/text()|.//h2/a/text()")
    link = item.xpath(".//a[not(contains(@class,'topic-title-pic'))]/@href|.//h2/a/@href")
    date = item.xpath(".//a[not(contains(@class,'topic-title-pic'))]/time/@datetime|.//h2/a/time/@datetime")

    le_news['name'] = name[0]
    le_news['link'] = url + link[0] if link[0].count('https:') == 0 else link[0]
    le_news['source'] = "lenta.ru"
    le_news['date'] = date[0]

    le_newss.append(le_news)

lenta = db.lenta

lenta.insert_many(le_newss)

for news in lenta.find({}):
    pprint(news)

# https://news.mail.ru/

url = 'https://news.mail.ru/'

response = requests.get(url, headers=header)
dom = html.fromstring(response.text)

links = dom.xpath("//div[@data-module='TrackBlocks' and @class='js-module']//a[not(contains(@class,'banner'))]/@href")
links = frozenset(links)

nm_newss = []
for li in links:
    response = requests.get(li, headers=header)
    dom = html.fromstring(response.text)

    nm_news = {}
    name = dom.xpath("//h1/text()")
    nm_link = li
    source = dom.xpath("//span[@class='note']/a/span/text()")
    date = dom.xpath("//span[@class='note']/span[@datetime]/@datetime")

    nm_news['name'] = name[0]
    nm_news['link'] = nm_link
    nm_news['source'] = source[0]
    nm_news['date'] = date[0]

    nm_newss.append(nm_news)

news_mail = db.news_mail

news_mail.insert_many(nm_newss)

for news in news_mail.find({}):
    pprint(news)
