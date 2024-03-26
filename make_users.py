from flask import Flask
from data import db_session
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

# Добавляем капитана
def main():
    db_session.global_init("db/mars_explorer.db")
    session = db_session.create_session()

    user = User()
    user.surname = "Scott"
    user.name = "Ridley"
    user.age = 21
    user.position = "captain"
    user.speciality = "research engineer"
    user.address = "module_1"
    user.email = "scott_chief@mars.org"
    user.hashed_password = "cap"
    user.set_password(user.hashed_password)
    session.add(user)
    
    user = User()
    user.surname = "Шах"
    user.name = "Матович"
    user.age = 1
    user.position = "шестерка"
    user.speciality = "research engineer"
    user.address = "module_1"
    user.email = "умпа@лумпа.com"
    user.hashed_password = "cringe"
    user.set_password(user.hashed_password)
    session.add(user)
    
    user = User()
    user.surname = "Лицей"
    user.name = "Учинормально"
    user.age = 1000
    user.position = "ужас"
    user.speciality = "engineer"
    user.address = "module_2"
    user.email = "аран@гутанг.com"
    user.hashed_password = "lizei-diz"
    user.set_password(user.hashed_password)
    session.add(user)

    user = User()
    user.surname = "Неприх"
    user.name = "Одитеналицей"
    user.age = 404
    user.position = "ошибка"
    user.speciality = "biolog"
    user.address = "module_1"
    user.email = "лицей@dead.ru"
    user.hashed_password = "smert_v_lizee"
    user.set_password(user.hashed_password)
    session.add(user)

    session.commit()


if __name__ == '__main__':
    main()
