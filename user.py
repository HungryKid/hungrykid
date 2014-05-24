from sqlalchemy import Table, MetaData, Column, types
from sqlalchemy.orm import mapper

class User(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
		return "User<'%d','%s'>" % (self.id, self.name)


metadata = MetaData()

users = Table('user', metadata,
    Column('id', types.Integer, primary_key=True),
    Column('name', types.String(50)),
)

mapper(User, users)