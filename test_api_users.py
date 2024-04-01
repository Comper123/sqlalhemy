from requests import put, get, post, delete


# GET запросы
# print(get('http://127.0.0.1:5000/api/v2/users').json())
# print(get('http://127.0.0.1:5000/api/v2/users/2').json())
# print(get('http://127.0.0.1:5000/api/v2/users/100').json())
# print(get('http://127.0.0.1:5000/api/v2/users/привет').json())


# POST запросы
# print(post('http://127.0.0.1:5000/api/v2/users', json={
    # 'surname': 'Бабуров', 
    # 'name': 'Иван', 
    # 'age': 17,
    # 'position': 'чепух',
    # 'speciality': 'чиллить',
    # 'address': 'вн',
    # 'email': 'ivan@email.com',
    # 'city_from': 'Великий Новгород'
# }).json())
# print(post('http://127.0.0.1:5000/api/v2/users', json={}))
# print(post('http://127.0.0.1:5000/api/v2/users', json={
#     'name': 'Илья'
# }))


# DELETE запросы
# print(delete('http://127.0.0.1:5000/api/v2/users/11').json())
# print(delete('http://127.0.0.1:5000/api/v2/users/110').json())


# PUT запросы
# print(put('http://127.0.0.1:5000/api/v2/users/11', json={
#     'surname': 'Бабуров', 
#     'name': 'абоба', 
#     'age': 17,
#     'position': 'чепух',
#     'speciality': 'чиллить',
#     'address': 'вн',
#     'email': 'ivan@email.com',
#     'city_from': 'Великий Новгород'
# }).json())
# print(put('http://127.0.0.1:5000/api/v2/users/11', json={}).json())
# print(put('http://127.0.0.1:5000/api/v2/users/11', json={
#     "gg": 'gh'
# }).json())
# print(put('http://127.0.0.1:5000/api/v2/users/11', json={
#     "name": 'Илья'
# }).json())