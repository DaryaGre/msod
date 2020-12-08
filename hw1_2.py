#2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis).
# Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию.
# Ответ сервера записать в файл.

# Artsy.net - онлайн-галерея, в которой продается искусство тысяч художников со всего мира.
import requests
import json

client_id = 'e70348cedcec3e5a11f9'
client_secret = '1cb22b273229a3b66cbd4b9e20b8ec34'

main_link = f'https://api.artsy.net/api/tokens/xapp_token?client_id={client_id}&client_secret={client_secret}'

# получение токена
response_t = requests.post(main_link)

if response_t.ok:
    token = response_t.json()['token']

    headers = {'Content-Type': 'application/json',
               'X-XAPP-Token': token
               }
    # получение случайного профиля художника
    response = requests.get('https://api.artsy.net/api/shows?status=upcoming&sample=1', headers=headers)

    if response.ok:
        with open(f"Artsy.json", "w", encoding='UTF-8') as write_f:
            json.dump(response.json(), write_f, indent=4, ensure_ascii=False)
