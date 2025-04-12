import sqlalchemy
from data.db_session import SqlAlchemyBase
from sqlalchemy import orm


class Genre(SqlAlchemyBase):
    __tablename__ = "genres"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    novels_genres = orm.relationship('NovelGenre', back_populates='genre')
