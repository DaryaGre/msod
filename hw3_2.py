
from pprint import pprint
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)

db = client['hh_ru']

vacancys_hh_test = db.vacancys_hh_test

while True:
    salary = input('Введите желаемую зарплату: ')
    try:
        salary=int(salary)
        break
    except:
        print("Зарплата должна быть целым числом")

for vacancy in vacancys_hh_test.find({'$or':[{'salary_min':{'$gte':salary}},{'salary_max':{'$gte':salary}}]}):
     pprint(vacancy)