from sqlalchemy import Table, MetaData, Column, types
from sqlalchemy.orm import mapper
import datetime

class Shop(object):
    def __init__(self, id, name, type, latitude, longitude, photo, weight,url, phone,address):
        self.shopid = id
        self.name = name
        self.type = type
        self.latitude = latitude # ido
        self.longitude = longitude # keido
        self.photo = photo
        self.weight = weight
        self.url = url
        self.phone = phone
        self.address = address
    #def __repr__(self):
    #    return
    @classmethod
    def nophoto(self, id, name, type, latitude, longitude, weight):
        self.shopid = id
        self.name = name
        self.type = type
        self.latitude = latitude # ido
        self.longitude = longitude # keido
        self.weight = weight

metadata = MetaData()

shops = Table('shop', metadata,
        Column('id', types.Integer, primary_key=True, autoincrement=True),
        Column('shopid', types.String(50), primary_key=True),
        Column('name', types.String(100)),
        Column('type', types.String(20)),
        Column('latitude', types.Float),
        Column('longitude', types.Float),
        Column('photo', types.String(500), nullable=True),
        Column('weight', types.Integer),
        Column('url', types.String(100)),
        Column('phone', types.String(20)),
        Column('address', types.String(100)),
        #Column('review', types.String(100)),
        Column('date', types.DateTime, default=datetime.datetime.utcnow()),
        )
mapper(Shop, shops)
