from flask import Flask
from data import db_session
from data.jobs import Jobs


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/mars_explorer.db")
    session = db_session.create_session()

    job = Jobs()
    job.team_leader = 3
    job.job = "meet new astronauts"
    job.work_size = 1
    job.collaborators = str([1, 4])
    job.start_date
    job.is_finished = False
    session.add(job)

    session.commit()

if __name__ == "__main__":
    main()