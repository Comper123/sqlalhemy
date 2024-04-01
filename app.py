from flask import Flask, jsonify
from flask import render_template # Функция возвращения шаблона
from flask import request, redirect, abort
from flask_login import LoginManager # Авторизация
from flask_login import login_user, login_required, logout_user, current_user # Функция авторизации
from flask import make_response
import requests
from os import listdir
from flask_restful import Api

from data import db_session # Сессия с базой данных
from forms.login import LoginForm # Форма авторизации
from data.jobs import Jobs # Модель работы
from data.users import User # Модель пользователя
from forms.register import RegisterForm # Форма регистрации
from forms.job import JobForm # Форма работы
from data.departments import Department
from forms.department import DepartmentForm
import api
import users_api

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

api2 = Api(app)

# Настройки для авторизации пользователей
login_manager = LoginManager()
login_manager.init_app(app)
yandex_geocoder_api_key = '40d1649f-0493-4b70-98ba-98533de7710b'


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
        login_user(user)
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


@app.route('/addjob', methods=['POST', 'GET'])
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        job = Jobs(
            job=form.job.data,
            work_size=form.work_size.data,
            team_leader=current_user.id,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data
        )
        session = db_session.create_session()
        session.add(job)
        session.commit()
        return redirect('/')
    return render_template('addjob.html', form=form, title='Добавить работу')
    

@app.route('/job/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = JobForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id).first()
        if job:
            form.job.data = job.job
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.is_finished.data = job.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id).first()
        if job:
            job.job = form.job.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('addjob.html',
                           title='Редактирование работы',
                           form=form
                           )


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id).first()
    if job:
        db_sess.delete(job)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/departments')
def departments():
    session = db_session.create_session()
    data = {
        "departments": session.query(Department).all(),
        "users": {user.id: f"{user.surname} {user.name}" for user in session.query(User).all()}
    }
    return render_template('departments.html', data=data)


@app.route('/adddepartment', methods=['POST', 'GET'])
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        dep = Department(
            title=form.title.data,
            chief=current_user.id,
            members=form.members.data,
            email=form.email.data
        )
        session = db_session.create_session()
        session.add(dep)
        session.commit()
        return redirect('/departments')
    return render_template('adddepartment.html', form=form, title='Добавить отдел')
    

@app.route('/department/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    form = DepartmentForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        dep = db_sess.query(Department).filter(Department.id == id).first()
        if dep:
            form.title.data = dep.title
            form.members.data = dep.members
            form.email.data = dep.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dep = db_sess.query(Department).filter(Department.id == id).first()
        if dep:
            dep.title = form.title.data
            dep.members = form.members.data
            dep.email = form.email.data
            db_sess.commit()
            return redirect('/departments')
        else:
            abort(404)
    return render_template('adddepartment.html',
                           title='Редактирование отдела',
                           form=form
                           )


@app.route('/departments_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def department_delete(id):
    db_sess = db_session.create_session()
    dep = db_sess.query(Department).filter(Department.id == id).first()
    if dep:
        db_sess.delete(dep)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/departments')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.route('/users_show/<int:user_id>')
def show_user_city(user_id):
    try:
        user = requests.get(f'http://127.0.0.1:5000/api/users/{user_id}').json()['user']
        if user['city_from'] + ".png" not in [f for f in listdir('./static/img')]:
            link = f'http://geocode-maps.yandex.ru/1.x/?apikey={yandex_geocoder_api_key}&geocode={user["city_from"]}&format=json'
            response = requests.get(link)
            if response:
                data = response.json()
                object = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                coords = list(map(float, object["Point"]["pos"].split()))
                x, y = coords

                map_link = f"https://static-maps.yandex.ru/1.x/?ll={x},{y}&l=map&z=10"
                content = requests.get(map_link).content
                map_file = f"./static/img/{user['city_from']}.png"
                with open(map_file, 'wb') as map_1:
                    map_1.write(content)
            else:
                abort(404, message=f"Такого города не существует")
    except KeyError:
        abort(404, message=f"Пользователь не найден")
        
    data = {
        'user': f"{user['name']} {user['surname']}",
        'city': user["city_from"],
        'img': f"img/{user['city_from']}.png"
    }
    return render_template('city.html', data=data)


# для списка объектов
api2.add_resource(users_api.UserListResource, '/api/v2/users') 

# для одного объекта
api2.add_resource(users_api.UserResource, '/api/v2/users/<int:user_id>')


if __name__ == '__main__':
    app.register_blueprint(api.blueprint)
    main()