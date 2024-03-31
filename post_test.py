from requests import post, get, put


# Пустой запрос
print(post('http://127.0.0.1:5000/api/jobs', json={}).json())


# Неправильный запрос
print(post('http://127.0.0.1:5000/api/jobs',
           json={'job': 'Заголовок'}).json())


# Правильный запрос
print(post('http://127.0.0.1:5000/api/jobs',
           json={'job': 'Сбор ягод',
                 'work_size': 10,
                 'collaborators': '1, 2, 3',
                 'is_finished': True,
                 'team_leader': 10}).json())


# Проверка
print(get('http://127.0.0.1:5000/api/jobs').json())