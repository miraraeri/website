import sqlalchemy
from data.db_session import SqlAlchemyBase
from sqlalchemy import orm


class AgeLimit(SqlAlchemyBase):
    __tablename__ = 'age_limits'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    novels = orm.relationship('Novel', back_populates='age_limit')