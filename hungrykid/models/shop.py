from sqlalchemy import Table, MetaData, Column, types
from sqlalchemy.orm import mapper

class Shop(object):
    def __init__(self, id, name, type, latitude, longitude, weight):
        self.shopid = id
        self.name = name
        self.type = type
        self.latitude = latitude # ido
        self.longitude = longitude # keido
        self.weight = weight

    #def __repr__(self):
    #    return

metadata = MetaData()

shops = Table('shop', metadata,
        Column('id', types.Integer, primary_key=True, autoincrement=True),
        Column('shopid', types.String(50), primary_key=True),
        Column('name', types.String(100)),
        Column('type', types.String(20)),
        Column('latitude', types.Float),
        Column('longitude', types.Float),
        Column('weight', types.Integer),
        )
mapper(Shop, shops)
