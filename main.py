from flask import Flask, render_template, redirect, url_for, request, session
import data.db_session as db_session
from data.db_session import global_init
from data.users import User
from forms.register import RegisterForm
from forms.login import LoginForm
from forms.edit_profile import EditUserForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

USER = None
SAVE_USER = None

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form, message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form, message="Такой пользователь уже есть")
        user = User(
            username=form.username.data,
            birth_date=form.birth_date.data,
            email=form.email.data,
            avatar=form.avatar.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global USER
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if not db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('login.html', title='Авторизация', form=form,
                                       message="Такого пользователя нет")
        else:
            user = db_sess.query(User).filter_by(email=form.email.data).first()
            if not user.check_password(form.password.data):
                return render_template('login.html', title='Авторизация', form=form,
                                       message="Неверный пароль")
        if form.remember_me:
            pass
        session['user_id'] = user.id
        return redirect('/main_page')
    return render_template('login.html', title="Авторизация", form=form)


@app.route('/')
@app.route('/main_page')
def main_page():
    if 'user_id' in session:
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter_by(id=session['user_id']).first()
        return render_template('base.html', title='Главная страница', username=user.username)
    return render_template('base.html', title='Главная страница')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return render_template('base.html', title='Главная страница', message="Вы не вошли в аккаунт")
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter_by(id=session['user_id']).first()
    param = {
        'title': 'Профиль',
        'username': user.username,
        'birth_date': user.birth_date,
        'modified_date': user.modified_date
    }
    return render_template('profile.html', **param)


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        return redirect('/login')
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter_by(id=session['user_id']).first()
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.avatar = form.avatar.data
        user.birth_date = form.birth_date.data

        if form.password.data:
            user.set_password(form.password.data)
        db_sess.commit()
        db_sess.refresh(user)
        return redirect('/profile')
    return render_template('edit_profile.html', title='Редактирование', form=form)


def main():
    global_init('db/web_novel.db')
    app.run()


if __name__ == '__main__':
    main()
