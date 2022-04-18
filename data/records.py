from datetime import date
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
import uuid
import cryptocode


class Record(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'record'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    record_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    parameter = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    date_ = sqlalchemy.Column(sqlalchemy.String,
                                     default=str(date.today()))
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