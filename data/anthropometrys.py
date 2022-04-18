from datetime import date
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
import uuid
import cryptocode


class Anthropometry(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'anthropometry'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    height = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    weight = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    waist = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    hip_girth = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    bust = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    date_ = sqlalchemy.Column(sqlalchemy.String,
                                     default=str(date.today()))
    photo = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')

    def hashing(self, parameter):
        with open('keys.txt', 'r', encoding='utf-8') as file:
            key = file.read()
            str_encoded = cryptocode.encrypt(parameter, key)
        return str_encoded

    def rehashing(self, parameter):
        with open('keys.txt', 'r', encoding='utf-8') as file:
            key = file.read()
            str_decoded = cryptocode.decrypt(parameter, key)
        return str_decoded