import argparse
from flask import Flask
from data import db_session
from data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

parser = argparse.ArgumentParser()
parser.add_argument("db_name")

args = parser.parse_args()


def main():
    db_session.global_init(args.db_name)
    session = db_session.create_session()
    for job in session.query(Jobs).filter(Jobs.work_size < 20,
                                           Jobs.is_finished == False):
        print(f"<Job> {job.job}")
    
    session.commit()


if __name__ == '__main__':
    main()
