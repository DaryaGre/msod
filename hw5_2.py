from selenium import webdriver
import time
from pprint import pprint
from pymongo import MongoClient

driver = webdriver.Chrome()

driver.get('https://www.mvideo.ru/')

hits = driver.find_element_by_xpath("//div[contains(text(),'Хиты продаж')]/ancestor::div[@class='section']")

next = hits.find_element_by_class_name('next-btn')
li_last = 0

while True:
    li = hits.find_elements_by_class_name('sel-product-tile-title')

    if len(li) > li_last:
        li_last = len(li)
        next.click()
        time.sleep(5)
    else:
        break

client = MongoClient('127.0.0.1', 27017)

db = client['m_video']

mv_hits = db.mv_hits

for elem in li:
    hit = {"productPriceLocal":elem.get_attribute('data-product-info').split('\n')[1].replace('\t','').replace(',','').split(': ')[1].replace('"',''),
           "productName":elem.get_attribute('data-product-info').split('\n')[3].replace('\t', '').replace(',', '').split(': ')[1].replace('"',''),
           "productCategoryName":elem.get_attribute('data-product-info').split('\n')[5].replace('\t', '').replace(',', '').split(': ')[1].replace('"',''),
           "productVendorName":elem.get_attribute('data-product-info').split('\n')[6].replace('\t', '').replace(',', '').split(': ')[1].replace('"','')
           }
    mv_hits.insert_one(hit)


for m in mv_hits.find({}):
    pprint(m)


driver.close()