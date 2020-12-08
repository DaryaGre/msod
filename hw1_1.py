# 1. Посмотреть документацию к API GitHub,
# разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

import requests
import json

user = input('Введите имя пользователя: ')

main_link = f'https://api.github.com/users/{user}/repos'

response = requests.get(main_link)

if response.ok:
    with open(f"{user}_repos.json", "w", encoding='UTF-8') as write_f:
        json.dump(response.json(), write_f, indent=4, ensure_ascii=False)
