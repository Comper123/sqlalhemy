from requests import put, get, post, delete


# GET запросы
# print(get('http://127.0.0.1:5000/api/v2/jobs').json())
# print(get('http://127.0.0.1:5000/api/v2/jobs/0').json())
# print(get('http://127.0.0.1:5000/api/v2/jobs/100').json())
# print(get('http://127.0.0.1:5000/api/v2/jobs/привет').json())


# POST запросы
# print(post('http://127.0.0.1:5000/api/v2/jobs', json={
    # 'job': 'kill monsters', 
    # 'collaborators': '1, 7', 
    # 'work_size': 3,
    # 'is_finished': False,
    # 'team_leader': 1,
# }).json())
# print(post('http://127.0.0.1:5000/api/v2/jobs', json={}))
# print(post('http://127.0.0.1:5000/api/v2/jobs', json={
#     'job': 'Илья'
# }))


# DELETE запросы
# print(delete('http://127.0.0.1:5000/api/v2/jobs/11').json())
# print(delete('http://127.0.0.1:5000/api/v2/jobs/110').json())


# PUT запросы
# print(put('http://127.0.0.1:5000/api/v2/jobs/10', json={
#     'job': 'kill monsters', 
#     'collaborators': '1, 7, 9', 
#     'work_size': 3,
#     'is_finished': False,
#     'team_leader': 1,
# }).json())
# print(put('http://127.0.0.1:5000/api/v2/users/10', json={}).json())
# print(put('http://127.0.0.1:5000/api/v2/users/10', json={
#     "gg": 'gh'
# }).json())
# print(put('http://127.0.0.1:5000/api/v2/users/1', json={
#     "name": 'Илья'
# }).json())