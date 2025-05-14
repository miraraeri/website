import datetime

from flask import Flask, render_template, redirect, request, session, send_from_directory, flash, get_flashed_messages, url_for
import data.db_session as db_session
from data.db_session import global_init
from data.users import User
from data.genres import Genre
from data.novels import Novel
from data.novels_genres import NovelGenre
from data.age_limits import AgeLimit
from data.novels_pics import NovelsPics
from forms.register import RegisterForm
from forms.login import LoginForm
from forms.create_novel import CreateNovel
from forms.edit_novel import EditNovel
from forms.edit_profile import EditUserForm
from forms.simple_search import SimpleSearch
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=90)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация прекрасного пользователя',
                                   form=form, message="Увы, но пароли должны совпадать")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация прекрасного пользователя',
                                   form=form, message="Ах, такой пользователь уже есть")
        f = request.files.get('avatar')
        if f.content_type not in ['image/jpeg', 'image/png']:
            return render_template('register.html', title='Регистрация прекрасного пользователя',
                                   form=form)
        ava_path = os.path.join('static/user_avatars', f.filename)
        f.save(ava_path)
        user = User(
            username=form.username.data,
            birth_date=form.birth_date.data,
            email=form.email.data,
            avatar=ava_path
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация прекрасного пользователя', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if not db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('login.html', title='Авторизация прекрасного пользователя',
                                   form=form, message="Печально, но такого пользователя нет")
        else:
            user = db_sess.query(User).filter_by(email=form.email.data).first()
            if not user.check_password(form.password.data):
                return render_template('login.html', title='Авторизация прекрасного пользователя',
                                       form=form, message="У вас был другой пароль")
        if form.remember_me:
            session.permanent = True
        else:
            session.permanent = False
        session['user_id'] = user.id
        return redirect('/main_page')
    return render_template('login.html', title="Авторизация прекрасного пользователя", form=form)


@app.context_processor
def inject_search_form():
    return dict(search_form=SimpleSearch())


@app.before_request
def handle_search():
    form = SimpleSearch()
    if form.validate_on_submit() and 'simple_search' in request.form:
        query = form.simple_search.data
        return redirect(url_for('main_page', q=query))


@app.route('/')
@app.route('/main_page')
def main_page():
    query = request.args.get('q')
    db_sess = db_session.create_session()
    if query:
        novels = db_sess.query(Novel).filter(Novel.name.like(f'%{query}%') | (Novel.description.like(f'%{query}%')) |
                                             (User.username.like(f'%{query}%'))).all()
    else:
        novels = db_sess.query(Novel)

    if 'user_id' in session:
        user = db_sess.query(User).filter_by(id=session['user_id']).first()
        if user is not None:
            clean_avatar = user.avatar.replace('\\', '/').replace('static', '')
            return render_template('main_page.html', title='Главная страница', user=user,
                                   username=user.username, avatar=url_for('static', filename=clean_avatar),
                                   novels=novels, query=query)
        else:
            session.pop('user_id', None)
    return render_template('main_page.html', title='Главная страница', novels=novels, query=query)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return render_template('base.html', title='Главная страница')
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter_by(id=session['user_id']).first()
    clean_avatar = user.avatar.replace('\\', '/').replace('static', '')
    param = {
        'title': 'Профиль прекрасного пользователя',
        'username': user.username,
        'birth_date': user.birth_date,
        'modified_date': user.modified_date,
        'avatar': url_for('static', filename=clean_avatar)
    }
    if request.method == 'POST':
        if user is not None:
            session['user_id'] = None
            return redirect('/')
        else:
            return redirect('/login')
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
        user.birth_date = form.birth_date.data
        f = request.files['avatar']

        if f and f.content_type in ['image/jpeg', 'image/png']:
            ava_path = os.path.join('static/user_avatars', f.filename)
            f.save(ava_path)
            user.avatar = ava_path

        if form.password.data:
            user.set_password(form.password.data)
        db_sess.commit()
        db_sess.refresh(user)
        return redirect('/profile')
    return render_template('edit_profile.html', title='Редактирование лучшего профиля', form=form)


@app.route('/del_profile', methods=['GET', 'POST'])
def del_profile():
    if 'user_id' not in session:
        return redirect('/login')
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter_by(id=session['user_id']).first()
    if request.method == 'POST':
        if user is not None:
            session['user_id'] = None
            db_sess.delete(user)
            db_sess.commit()
            return redirect('/')
        else:
            return redirect('/login')
    return render_template('del_profile.html', title='Удаление аккаунта прекрасного пользователя')


@app.route('/create_novel', methods=['GET', 'POST'])
def create_novel():
    if 'user_id' not in session:
        return redirect('/login')
    form = CreateNovel()
    db_sess = db_session.create_session()
    genres = db_sess.query(Genre).all()
    age_limits = db_sess.query(AgeLimit).all()
    genres_list = [g.name for g in genres]
    ages_list = [al.name for al in age_limits]
    if form.validate_on_submit():
        user = db_sess.query(User).filter_by(id=session['user_id']).first()
        age_limit_id = db_sess.query(AgeLimit).filter_by(name=form.age_limit.data).first()
        f = request.files['novel_arch']
        if f.content_type not in ['application/x-compressed', 'application/zip', 'application/x-zip-compressed', 'application/x-rar-compressed', 'application/x-7z-compressed']:
            return redirect(request.url)
        novel_path = os.path.join('static/novel_archive', f.filename)
        novel_path = novel_path.replace('\\', '/')

        novel_ava = request.files['novel_avatar']
        if novel_ava.content_type not in ['image/jpeg', 'image/png']:
            return render_template('create_novel.html', title='Создать новую новеллу', form=form,
                                   genres=genres_list, age_limits=ages_list)
        novel_ava_path = os.path.join('static/novel_avatars', novel_ava.filename)
        novel_ava_path = novel_ava_path.replace('\\', '/')

        novel_pics = form.novel_pics.data
        pics_paths = []
        for pic in novel_pics:
            if pic.content_type not in ['image/jpeg', 'image/png', 'image/gif', 'video/mp4', 'video/x-msvideo', 'video/quicktime', 'video/x-matroska']:
                return render_template('create_novel.html', title='Создать новую новеллу', form=form,
                                       genres=genres_list, age_limits=ages_list)
            pic_path = os.path.join('static/novel_pics', pic.filename)
            pic_path = pic_path.replace('\\', '/')
            pics_paths.append(pic_path)

        novel = Novel(
            name=form.name.data,
            description=form.desc.data,
            creation_date=form.creation_date.data,
            archive_url=novel_path,
            novel_avatar=novel_ava_path
        )
        db_sess.add(novel)
        db_sess.flush()
        if not request.form.getlist('genre'):
            db_sess.rollback()
            return render_template('create_novel.html', title='Создать новую новеллу', form=form,
                                   genres=genres_list, age_limits=ages_list, message='Добавьте жанры, без них никуда')

        for genre in request.form.getlist('genre'):
            print(genre)
            n_genre = db_sess.query(Genre).filter_by(name=genre).first()
            novel_genre = NovelGenre(novel_id=novel.id, genre_id=n_genre.id)
            db_sess.add(novel_genre)
        user.novels.append(novel)
        age_limit_id.novels.append(novel)

        for path in pics_paths:
            novels_pics = NovelsPics(
                pic_path=path,
                novel=novel
            )
            db_sess.add(novels_pics)

        f.save(novel_path)
        novel_ava.save(novel_ava_path)
        for i in range(len(pics_paths)):
            novel_pics[i].save(pics_paths[i])
        db_sess.commit()
        return redirect('/')
    return render_template('create_novel.html', title='Создать новую новеллу', form=form,
                           genres=genres_list, age_limits=ages_list)


@app.route('/novel_profile/<int:id_novel>')
def novel_profile(id_novel):
    db_sess = db_session.create_session()
    novel = db_sess.query(Novel).filter_by(id=id_novel).first()
    if novel is None:
        return redirect('/error')
    novel_genres = db_sess.query(NovelGenre).filter_by(novel_id=id_novel).all()
    genres = [g.genre.name for g in novel_genres]
    novel_pics = db_sess.query(NovelsPics).filter_by(novel_id=id_novel).all()
    pics = []
    for pic in novel_pics:
        clean_pic = pic.pic_path.replace('\\', '/').replace('static', '')
        pics.append(url_for('static', filename=clean_pic))
    clean_novel_ava = novel.novel_avatar.replace('\\', '/').replace('static', '')
    param = {
        'title': "Прекрасная новелла",
        'name': novel.name,
        'creator': novel.user.username if novel.user else 'Неизвестно',
        'genres': genres,
        'age_limit': novel.age_limit.name,
        'desc': novel.description,
        'novel_id': novel.id,
        'novel_user_id': novel.user_id,
        'novel_ava': url_for('static', filename=clean_novel_ava),
        'pics': pics
    }
    if 'user_id' in session:
        user = db_sess.query(User).filter_by(id=session['user_id']).first()
        param['user'] = user
        param['username'] = user.username
        param['user_id'] = user.id
        clean_avatar = user.avatar.replace('\\', '/').replace('static', '')
        param['avatar'] = url_for('static', filename=clean_avatar)
    return render_template('novel_profile.html', **param)


@app.route('/download/<int:id_novel>')
def download(id_novel):
    if 'user_id' not in session:
        return redirect(f'/novel_profile/{id_novel}')
    db_sess = db_session.create_session()
    novel = db_sess.query(Novel).filter(Novel.id==id_novel).first()
    novel_arch = novel.archive_url
    if not novel_arch:
        return 'Такого файла не существует'
    filename = os.path.basename(novel_arch)
    directory = os.path.abspath(os.path.dirname(novel_arch))
    return send_from_directory(directory, filename, as_attachment=True)


@app.route('/edit_novel/<int:id_novel>', methods=['GET', 'POST'])
def edit_novel(id_novel):
    if 'user_id' not in session:
        return redirect('/login')
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter_by(id=session['user_id']).first()
    novel = db_sess.query(Novel).filter_by(id=id_novel).first()
    if novel is None:
        return redirect('/error')
    if user.id != novel.user_id:
        return redirect('/')
    age_limit = db_sess.query(AgeLimit).all()
    all_genre = db_sess.query(Genre).all()
    novel_genres = db_sess.query(NovelGenre).filter_by(novel_id=novel.id).all()

    form = EditNovel(obj=novel)
    form.age_limit.choices = [(al.id, al.name) for al in age_limit]
    form.genre.choices = [(g.id, g.name) for g in all_genre]
    if request.method == 'GET':
        form.age_limit.data = novel.age_limit_id
        form.genre.data = [g.genre_id for g in novel_genres]
        form.desc.data = novel.description

    if form.validate_on_submit():
        novel.name = form.name.data
        novel.age_limit_id = form.age_limit.data
        novel.description = form.desc.data
        f = request.files['novel_arch']
        if f and f.content_type in ['application/x-compressed', 'application/zip', 'application/x-zip-compressed', 'application/x-rar-compressed', 'application/x-7z-compressed']:
            clean_arch_path = os.path.join('static/novel_archive', f.filename)
            clean_arch_path = clean_arch_path.replace('\\', '/')
            f.save(clean_arch_path)
            novel.archive_url = clean_arch_path

        novel_ava = request.files['novel_ava']
        if novel_ava and novel_ava.content_type in ['image/jpeg', 'image/png']:
            clean_ava_path = os.path.join('static/novel_avatars', novel_ava.filename)
            clean_ava_path = clean_ava_path.replace('\\', '/')
            novel_ava.save(clean_ava_path)
            novel.novel_avatar = clean_ava_path

        novel_pics = form.novel_pics.data
        if form.del_old_scr.data:
            db_sess.query(NovelsPics).filter(NovelsPics.novel_id == id_novel).delete()
        for pic in novel_pics:
            if pic and pic.content_type in ['image/jpeg', 'image/png', 'image/gif', 'video/mp4', 'video/x-msvideo', 'video/quicktime', 'video/x-matroska']:
                pic_path = os.path.join('static/novel_pics', pic.filename)
                pic_path = pic_path.replace('\\', '/')
                pic.save(pic_path)
                n_pics = NovelsPics(
                    pic_path=pic_path,
                    novel=novel
                )
                db_sess.add(n_pics)

        db_sess.query(NovelGenre).filter(NovelGenre.novel_id == id_novel).delete()
        for genre_id in form.genre.data:
            novel.novels_genres.append(NovelGenre(novel_id=id_novel, genre_id=genre_id))
        db_sess.commit()
        return redirect(f'/novel_profile/{id_novel}')
    return render_template('edit_novel.html', title='Редактирование лучшей новеллы', form=form,
                           user=user, username=user.username, nusername=novel.user.username, novel_id=id_novel)


@app.route('/del_novel/<int:id_novel>', methods=['GET', 'POST'])
def del_novel(id_novel):
    if 'user_id' not in session:
        return redirect('/login')
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter_by(id=session['user_id']).first()
    novel = db_sess.query(Novel).filter_by(id=id_novel).first()
    if novel is None:
        return redirect('/error')
    if user.id != novel.user_id:
        return redirect('/')
    if request.method == 'POST':
        db_sess.query(NovelGenre).filter(NovelGenre.novel_id == id_novel).delete()
        db_sess.query(NovelsPics).filter(NovelsPics.novel_id == id_novel).delete()
        db_sess.query(Novel).filter(Novel.id == id_novel).delete()
        db_sess.commit()
        return redirect('/')
    return render_template('del_novel.html', title="Удаление лучшей новеллы", user=user, username=user.username, novel_name=novel.name,
                           novel_id=novel.id)


@app.route('/error')
def error():
    return render_template('error.html')


def main():
    global_init('db/web_novel.db')
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()
