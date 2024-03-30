import argparse
from flask import Flask
from data import db_session
from data.jobs import Jobs
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

parser = argparse.ArgumentParser()
parser.add_argument("db_name")

args = parser.parse_args()


def main():
    db_session.global_init(args.db_name)
    session = db_session.create_session()
    jobs = [job for job in session.query(Jobs)]
    maxx_collaborators = max(len(j.collaborators.split(',')) for j in jobs)
    leaders = list(filter(lambda x: len(x.collaborators.split(',')) == maxx_collaborators,
                    jobs))
    leaders = [int(i.team_leader) for i in leaders]
    for user in session.query(User).filter(User.id.in_(leaders)):
        print(user.name, user.surname)
    session.commit()


if __name__ == '__main__':
    main()
