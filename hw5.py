from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
from pprint import pprint
from pymongo import MongoClient

driver = webdriver.Chrome()

driver.get('https://mail.ru/')

elem = driver.find_element_by_name('login')
elem.send_keys('study.ai_172')

elem.send_keys(Keys.ENTER)

elem = WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.NAME, 'password'))
        )
elem.send_keys('NextPassword172')

elem.send_keys(Keys.ENTER)

elem = WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'llc__container'))
        )

elem.click()

mails=[]

while True:
    time.sleep(2)

    mail = {}

    sender = driver.find_element_by_class_name('letter-contact').text
    date = driver.find_element_by_class_name('letter__date').text
    topic = driver.find_element_by_tag_name('h2').text
    text = driver.find_element_by_class_name('letter-body__body-content').text

    mail['sender'] = sender
    mail['date'] = date
    mail['topic'] = topic
    mail['text'] = text

    mails.append(mail)

    try:
        nextend = driver.find_element(By.XPATH, '//span[contains(@class,"button2_arrow-down") and @disabled]')
        break
    except Exception as e:
        nextmail =  driver.find_element_by_class_name('portal-menu-element_next')
        nextmail.click()

client = MongoClient('127.0.0.1', 27017)

db = client['mails']

mail_ru = db.mail_ru

mail_ru.insert_many(mails)

for m in mail_ru.find({}).limit(10):
    pprint(m)

driver.close()