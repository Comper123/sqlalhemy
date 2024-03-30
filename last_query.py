import argparse
from flask import Flask

from data import db_session
from data.users import User
from data.departments import Department
from data.jobs import Jobs


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
parser = argparse.ArgumentParser()
parser.add_argument("db_name")
args = parser.parse_args()


def main():
    db_session.global_init(args.db_name)
    session = db_session.create_session()
    users = session.query(Department).all()[0].members.split(", ")
    result = []
    jobs = session.query(Jobs).all()
    for user in users:
        works = 0
        for j in jobs:
            if user in j.collaborators.split(", "):
                works += j.work_size
        if works > 25:
            result.append(int(user))
    
    for user in session.query(User).filter(User.id.in_(result)):
        print(user.name, user.surname)

    session.commit()


if __name__ == '__main__':
    main()
