from requests import delete, post, put

# Правильный запрос
print(post('http://127.0.0.1:5000/api/jobs',
           json={'job': 'Сбор ягод',
                 'work_size': 10,
                 'collaborators': '1, 2, 3',
                 'is_finished': True,
                 'team_leader': 10}).json())

print(delete('http://127.0.0.1:5000/api/jobs/999').json())
# новости с id = 999 нет в базе

print(delete('http://127.0.0.1:5000/api/jobs/10').json())

