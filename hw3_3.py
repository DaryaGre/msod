from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
from pymongo import MongoClient

# https://hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&search_field=name&search_field=description&text=%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82&page=1
main_link = 'https://hh.ru/search/vacancy'


q = input('Введите вакансию: ')
page = 0
vacancys = []

client = MongoClient('127.0.0.1', 27017)

db = client['hh_ru']

vacancys_hh = db.vacancys_hh


while True:
    params = {'L_is_autosearch': 'false',
              'clusters': 'true',
              'enable_snippets': 'true',
              'search_field': 'name&search_field=escription',
              'text': q,
              'page': page}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

    response = requests.get(main_link, params=params, headers=headers)
    soup = bs(response.text, 'html.parser')

    if response.ok:
        vacancy_list = soup.findAll('div', {'class': 'vacancy-serp-item'})

        for vacancy in vacancy_list:
            vacancy_data = {}
            vacancy_info = vacancy.find('a')
            vacancy_name = vacancy_info.text
            vacancy_link = vacancy_info['href']
            #находим id вакансии для монго
            vacancy_id = vacancy_link.replace('https://hh.ru/vacancy/', '').split('?')[0]
            # Вот тут отбраковка данных уже добавленных в базу (впринципе можно было не создавать свой id а сделать проверку всех полей, но так кажется лучше)
            vacancy_search = list(vacancys_hh.find({'_id':(vacancy_id+'hh')}))
            if not vacancy_search==[]:
                continue
            vacancy_salary = vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'}).find("span")
            if vacancy_salary == None:
                vacancy_salary_max = None
                vacancy_salary_min = None
                vacancy_salary_cur = None
            elif vacancy_salary.text.find('-') != -1:
                vacancy_salary_min = vacancy_salary.text.split('-')[0].replace('\xa0', '')
                vacancy_salary_max = vacancy_salary.text.split('-')[1].split(' ')[0].replace('\xa0', '')
                vacancy_salary_cur = vacancy_salary.text.split('-')[1].split(' ')[1]
            else:
                if vacancy_salary.text.find('от') != -1:
                    vacancy_salary_min = vacancy_salary.text.split(' ')[1].replace('\xa0', '')
                    vacancy_salary_max = None
                    vacancy_salary_cur = vacancy_salary.text.split(' ')[2]
                elif vacancy_salary.text.find('до') != -1:
                    vacancy_salary_min = None
                    vacancy_salary_max = vacancy_salary.text.split(' ')[1].replace('\xa0', '')
                    vacancy_salary_cur = vacancy_salary.text.split(' ')[2]
                else:
                    vacancy_salary_max = None
                    vacancy_salary_min = None
                    vacancy_salary_cur = None

            vacancy_data['_id'] = (vacancy_id+'hh')
            vacancy_data['name'] = vacancy_name
            vacancy_data['link'] = vacancy_link
            vacancy_data['salary_max'] = vacancy_salary_max if vacancy_salary_max==None else int(vacancy_salary_max)
            vacancy_data['salary_min'] = vacancy_salary_min if vacancy_salary_min==None else int(vacancy_salary_min)
            vacancy_data['salary_cur'] = vacancy_salary_cur
            vacancy_data['site'] = 'hh.ru'

            vacancys.append(vacancy_data)
            vacancys_hh.insert_one(vacancy_data)
    if soup.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'}):
        page += 1
    else:
        break

#pprint(vacancys)
print(len(vacancys))

for vacancy in vacancys_hh.find({}).limit(3):
     pprint(vacancy)