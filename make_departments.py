from flask import Flask
from data import db_session
from data.departments import Department


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/mars_explorer.db")
    session = db_session.create_session()

    dep = Department()
    dep.title = "МВД"
    dep.chief = 1
    dep.members = "2, 4"
    dep.email = "hype@mail.ru"
    session.add(dep)

    session.commit()


if __name__ == "__main__":
    main()