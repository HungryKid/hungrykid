from sqlalchemy import Table, MetaData, Column, types
from sqlalchemy.orm import mapper

class Shop(object):
    def __init__(self, id, name, type, latitude, longitude):
        self.id = id
        self.name = name
        self.type = type
        self.latitude = latitude # ido
        self.longitude = longitude # keido

    #def __repr__(self):
    #    return

metadata = MetaData()

shops = Table('shop', metadata,
        # TODO use machine generated id?
#        Column('id', types.BigInteger, primary_key=True),
        Column('id', types.String(50), primary_key=True),
        Column('name', types.String(100)),
        Column('type', types.String(20)),
        Column('latitude', types.Float),
        Column('longitude', types.Float),
        )
mapper(Shop, shops)
