from flask import Flask
from flask import render_template # Функция возвращения шаблона
from flask import request, redirect
from flask_login import LoginManager # Авторизация
from flask_login import login_user, login_required, logout_user # Функция авторизации

from data import db_session
from forms.login import LoginForm # Форма авторизации
from data.jobs import Jobs # Модель работы
from data.users import User # Модель пользователя
from forms.register import RegisterForm # Форма регистрации


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

# Настройки для авторизации пользователей
login_manager = LoginManager()
login_manager.init_app(app)


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
        if form.pwd1.data != form.pwd2.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.login.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.login.data
        )
        user.set_password(form.pwd1.data)
        session.add(user)
        session.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


"""Для верной работы flask-login у нас должна быть функция для получения пользователя, 
украшенная декоратором login_manager.user_loader. Добавим ее:"""
@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

if __name__ == '__main__':
    main()