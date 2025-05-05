import sqlalchemy
from data.db_session import SqlAlchemyBase
from sqlalchemy import orm


class NovelsPics(SqlAlchemyBase):
    __tablename__ = 'novels_pics'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    pic_path = sqlalchemy.Column(sqlalchemy.String)
    novel_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('novels.id'))
    novel = orm.relationship('Novel')