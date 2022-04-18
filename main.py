from flask import Flask, render_template, redirect
from data import db_session
from forms.user import RegisterForm
from forms.user import RegisterForm
from data.users import User
from flask import Flask, render_template, redirect, request, abort
from data import db_session
from data.users import User
from forms.user import RegisterForm, LoginForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import users_api
from TOKENS import site_key, secret_key
from forms.anthropometry import AnthropometryForm
from data.anthropometrys import Anthropometry
from forms.record import RecordForm, RecordGetForm
from data.records import Record
import shutil
from datetime import date
from flask import url_for
from PIL import Image
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key_AF'

app.config['RECAPTCHA_PUBLIC_KEY'] = site_key
app.config['RECAPTCHA_PRIVATE_KEY'] = secret_key

login_manager = LoginManager()
login_manager.init_app(app)


def send_email(to, use_telegram, body="Спасибо за регистрацию!"):
    if use_telegram:
        body += "\nКстати, это наш бот, который вам поможет: http://t.me/athlete_factory_bot"
    # статичные данные
    smtp_host = "smtp.gmail.com"
    af_mail = "athlete.factory.messages@gmail.com"
    mail_login, mail_password = "athlete.factory.messages@gmail.com", "afga2022forgmailprostonado"
    # подключение и отправка сообщения
    server = smtplib.SMTP(host=smtp_host, port=587)
    server.starttls()
    server.login(mail_login, mail_password)
    server.sendmail(from_addr=af_mail, to_addrs=[to], msg=str(MIMEText(body, _charset="utf-8")), mail_options=(""))
    server.quit()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def start():
    # db_session.global_init("db/AF.db")
    return render_template('my_training.html')


@app.route('/my_training')
def my_training():
    return render_template('my_training.html')


# @app.route('/anthropometry')
# def anthropometry():
#     return render_template('anthropometry.html')


@app.route('/catalog')
def catalog():
    return render_template('catalog.html')


@app.route('/player')
def player():
    return render_template('player.html')


@app.route('/base_training')
def base_training():
    return render_template('promo_form.html')


@app.route('/fat_burning_training')
def fat_burning_training():
    return render_template('promo_form_burn.html')


@app.route('/power_training')
def power_training():
    return render_template('promo_form_power.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/catalog")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        email = form.email.data
        send_email(email, 'telegram')
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/anthropometry', methods=['GET', 'POST'])
@login_required
def add_anthropometry():
    form = AnthropometryForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        anthropometry_form = Anthropometry()
        if form.is_private.data:
            hashed_height = anthropometry_form.hashing(form.height.data)
            anthropometry_form.height = hashed_height
            hashed_weight = anthropometry_form.hashing(form.weight.data)
            anthropometry_form.weight = hashed_weight
            hashed_waist = anthropometry_form.hashing(form.waist.data)
            anthropometry_form.waist = hashed_waist
            hashed_hip_girth = anthropometry_form.hashing(form.hip_girth.data)
            anthropometry_form.hip_girth = hashed_hip_girth
            hashed_bust = anthropometry_form.hashing(form.bust.data)
            anthropometry_form.bust = hashed_bust
            anthropometry_form.is_private = form.is_private.data
        else:
            anthropometry_form.height = form.height.data
            anthropometry_form.weight = form.weight.data
            anthropometry_form.waist = form.waist.data
            anthropometry_form.hip_girth = form.hip_girth.data
            anthropometry_form.bust = form.bust.data
            anthropometry_form.is_private = form.is_private.data
        try:
            anthropometry_form.photo = True
            f = request.files['file']
            file = f.read()
            file_name = str(current_user.id) + str(date.today()) + "file.png"
            with open(f'static/images/{file_name}', "wb") as fi:
                fi.write(file)
            # shutil.move(file_name, f'static/images/{file_name}')
            # img = Image.open(f'static/images/{file_name}')
            # img.resize((350, 400))
            # img.save(f'static/images/{file_name}')
            # shutil.move(new_img, f'static/images/{file_name}')
        except Exception:
            anthropometry_form.photo = False
        current_user.anthropometry.append(anthropometry_form)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/catalog')
    return render_template('anthropometry.html', title='Добавление антропометрии',
                           form=form)


# @app.route('/get_anthropometry', methods=['GET', 'POST'])
# @login_required
# def get_anthropometry():
#     form = AnthropometryGetForm()
#     db_sess = db_session.create_session()
#     print(form.validate_on_submit())
#     if form.validate_on_submit():
#         print(1)
#         anthropometry = db_sess.query(Anthropometry).filter(Anthropometry.date_ == form.date_str.data).first()
#         # return render_template('get_anthropometry.html', title='Добавление антропометрии',
#         #                        form=form)
#         return render_template('get_anthropometry.html', title='Добавление антропометрии',
#                                form=form, anthropometry=anthropometry)
#     anthropometry = db_sess.query(Anthropometry).filter(Anthropometry.user_id == current_user.id)
#     for elems in anthropometry:
#         print(elems.height)
#     return render_template('get_anthropometry.html', title='Добавление антропометрии',
#                            form=form)
@app.route('/get_anthropometry', methods=['GET', 'POST'])
@login_required
def get_anthropometry():
    # form = AnthropometryGetForm()
    db_sess = db_session.create_session()
    if request.method == 'GET':
        return render_template('get_anthropometry.html', title='Добавление антропометрии')
    elif request.method == 'POST':
        date_anth = str(request.form['calendar'])
        anthropometry = db_sess.query(Anthropometry).filter(Anthropometry.date_ == date_anth,
                                                            Anthropometry.user_id == current_user.id).first()
        # for dates in db_sess.query(Anthropometry).filter(Anthropometry.user_id == current_user.id):
        #     print(dates.date_)
        # anth = db_sess.query(Anthropometry).filter(Anthropometry.user_id == current_user.id)
        # edit_anthropometry(anth)
        # return render_template('get_anthropometry.html', title='Добавление антропометрии',
        #                        form=form)
        if not anthropometry is None:
            if anthropometry.is_private:
                anthropometry_form = Anthropometry()
                anthropometry.height = anthropometry_form.rehashing(anthropometry.height)
                anthropometry.weight = anthropometry_form.rehashing(anthropometry.weight)
                anthropometry.waist = anthropometry_form.rehashing(anthropometry.waist)
                anthropometry.hip_girth = anthropometry_form.rehashing(anthropometry.hip_girth)
                anthropometry.bust = anthropometry_form.rehashing(anthropometry.bust)
        file_name = 'static/' + 'images/' + str(current_user.id) + str(date.today()) + "file.png"
        return render_template('get_anthropometry.html', title='Добавление антропометрии', anthropometry=anthropometry, file_name=file_name)


@app.route('/record', methods=['GET', 'POST'])
@login_required
def add_record():
    form = RecordForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        record_form = Record()
        if form.is_private.data:
            hashed_rec_name = record_form.hashing(form.rec_name.data)
            record_form.record_name = hashed_rec_name
            hashed_parameter = record_form.hashing(form.parameter.data)
            record_form.parameter = hashed_parameter
            record_form.is_private = form.is_private.data
        else:
            record_form.record_name = form.rec_name.data
            record_form.parameter = form.parameter.data
            record_form.is_private = form.is_private.data
        current_user.record.append(record_form)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/my_training')
    return render_template('record.html', title='Добавление рекорда',
                           form=form)


# @app.route('/get_record', methods=['GET', 'POST'])
# @login_required
# def get_record():
#     form = RecordGetForm()
#     db_sess = db_session.create_session()
#     anthropometry = db_sess.query(Anthropometry).filter(Record. == form.date_str.data, Anthropometry.user_id == current_user.id).first()
#     for dates in db_sess.query(Anthropometry).filter(Anthropometry.user_id == current_user.id):
#         print(dates.date_)
#     # anth = db_sess.query(Anthropometry).filter(Anthropometry.user_id == current_user.id)
#     # edit_anthropometry(anth)
#     # return render_template('get_anthropometry.html', title='Добавление антропометрии',
#     #                        form=form)
#     if not anthropometry is None:
#         if anthropometry.is_private:
#             anthropometry_form = Anthropometry()
#             anthropometry.height = anthropometry_form.rehashing(anthropometry.height)
#             anthropometry.weight = anthropometry_form.rehashing(anthropometry.weight)
#             anthropometry.waist = anthropometry_form.rehashing(anthropometry.waist)
#             anthropometry.hip_girth = anthropometry_form.rehashing(anthropometry.hip_girth)
#             anthropometry.bust = anthropometry_form.rehashing(anthropometry.bust)
#     return render_template('get_anthropometry.html', title='Добавление антропометрии',
#                            form=form, anthropometry=anthropometry)


def main():
    db_session.global_init("db/AF.db")
    app.register_blueprint(users_api.blueprint)
    app.run()


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    db_session.global_init("db/AF.db")
    app.run(host='0.0.0.0', port=port)