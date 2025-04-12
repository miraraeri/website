import datetime

import sqlalchemy
from data.db_session import SqlAlchemyBase
from sqlalchemy import orm


class Novel(SqlAlchemyBase):
    __tablename__ = 'novels'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    creation_date = sqlalchemy.Column(sqlalchemy.Date, default=datetime.date.today)
    archive_url = sqlalchemy.Column(sqlalchemy.String)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')
    age_limit_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("age_limits.id"))
    age_limit = orm.relationship('AgeLimit')
    novels_genres = orm.relationship('NovelGenre', back_populates='novel')
