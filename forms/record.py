from flask_wtf import FlaskForm, RecaptchaField
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField, SelectField
from wtforms.validators import DataRequired
from data.anthropometrys import Anthropometry
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session


class RecordForm(FlaskForm):
    rec_name = StringField('Введите название рекорда', validators=[DataRequired()])
    parameter = StringField('Укажите результат')
    is_private = BooleanField("Личное")
    submit = SubmitField('Добавить')


class RecordGetForm(FlaskForm):
    date_str = StringField('Введите название рекорда')
    submit = SubmitField('Получить данные')