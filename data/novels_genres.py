import sqlalchemy
from data.db_session import SqlAlchemyBase
from sqlalchemy import orm


class NovelGenre(SqlAlchemyBase):
    __tablename__ = 'novels_genres'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    novel_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('novels.id'))
    novel = orm.relationship('Novel')
    genre_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('genres.id'))
    genre = orm.relationship('Genre')