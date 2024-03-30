from flask import Flask, Blueprint 
from flask import render_template # Функция возвращения шаблона
from flask import request, redirect, abort
from flask_login import LoginManager # Авторизация
from flask_login import login_user, login_required, logout_user, current_user # Функция авторизации

from data import db_session # Сессия с базой данных
from forms.login import LoginForm # Форма авторизации
from data.jobs import Jobs # Модель работы
from data.users import User # Модель пользователя
from forms.register import RegisterForm # Форма регистрации
from forms.job import JobForm # Форма работы
from data.departments import Department
from forms.department import DepartmentForm
import api


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





if __name__ == '__main__':
    app.register_blueprint(api.blueprint)
    main()