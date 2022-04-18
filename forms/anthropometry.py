from flask_wtf import FlaskForm, RecaptchaField
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField, SelectField
from wtforms.validators import DataRequired
from data.anthropometrys import Anthropometry
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session


class AnthropometryForm(FlaskForm):
    height = StringField('Ваш рост', validators=[DataRequired()])
    weight = StringField('Ваш вес')
    waist = StringField('Обхват Вашей талии')
    hip_girth = StringField('Обхват Ваших бёдер')
    bust = StringField('Обхват Вашей груди')
    is_private = BooleanField("Личное")
    submit = SubmitField('Войти')


# class AnthropometryGetForm(FlaskForm):
#     date_str = StringField('Введите дату, в формате YY-MM-DD')
#     submit = SubmitField('Получить данные')


# class AnthropometryGetForm(FlaskForm):
#     date_str = SelectField('Category', choices=[], coerce=int)
#     submit = SubmitField('Получить данные')
#
#
# def edit_anthropometry(request, id):
#     user = Anthropometry.query.get(id)
#     form = AnthropometryGetForm(request.POST, obj=user)
#     form.date_str.choices = [(g.date) for g in Anthropometry.query.order_by('date_')]



# def edit_anthropometry(anthropometry):
#     for a in anthropometry:
#         print(a.date_)
#     lst = ['1', '2', '3']
#     form = AnthropometryGetForm()
#     form.date_str.choices = ['1', '2', '3']