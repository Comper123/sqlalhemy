import argparse
from flask import Flask
from data import db_session
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

parser = argparse.ArgumentParser()
parser.add_argument("db_name")

args = parser.parse_args()


def main():
    db_session.global_init(args.db_name)
    session = db_session.create_session()
    session.query(User).filter(User.address == "module_1",
                               User.age < 21). \
        update({'address': "module_3"})
    session.commit()


if __name__ == '__main__':
    main()
