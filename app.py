from flask import Flask
from data import db_session
from flask import render_template
from data.jobs import Jobs
from data.users import User
from forms.register import RegisterForm
from flask import request, redirect


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init('db/mars_explorer.db')
    app.run()


@app.route('/')
def jobs():
    session = db_session.create_session()
    data = {
        "jobs": session.query(Jobs).all(),
        "users": {user.id: f"{user.surname} {user.name}" for user in session.query(User).all()}
    }
    return render_template('jobs.html', data=data)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Записываем в бд результат формы
        
        return redirect('/')
    return render_template('register.html', form=form, title='Регистрация')


if __name__ == '__main__':
    main()