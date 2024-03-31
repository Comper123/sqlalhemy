import requests


# Получение всех работ
# print(requests.get('http://127.0.0.1:5000/api/jobs').json())


# Корректное получение одной работы
# print(requests.get('http://127.0.0.1:5000/api/jobs/0').json())


# Ошибочный запрос на получение одной работы — неверный id
# print(requests.get('http://127.0.0.1:5000/api/jobs/1').json())


# Ошибочный запрос на получение одной работы — строка
# print(requests.get('http://127.0.0.1:5000/api/jobs/привет').json())