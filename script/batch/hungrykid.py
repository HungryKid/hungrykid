#!/usr/bin/env python
# coding:utf-8

#
# google place api crawler
#
import urllib2
import json
import time

from sqlalchemy import create_engine, Table, MetaData, Column, types
from sqlalchemy.orm import scoped_session, sessionmaker, mapper
from sqlalchemy.orm.exc import NoResultFound

engine = create_engine('mysql+pymysql://hungry:imhungry@localhost/sandwich?charset=utf8', encoding='utf-8')

Session = scoped_session(sessionmaker(autocommit=False, autoflush=False,bind=engine))
db_session = Session()

# TODO insert db

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
metadata.create_all(engine)

apiurl = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
# TODO customize below parameters
parameter = 'location=35.6571942,139.7093825&radius=300&types=restaurant&sensor=false&rankby=prominence&'
key = 'xxx' # insert google api key here

# 1loop can get 20shops. 20x3loop=60shops are google place api restriction 
maxloop = 3 
sleeptime = 3

count = 0
shopcount = 0
nextpage = None
while count < maxloop:
    if nextpage is None:
        response = urllib2.urlopen(apiurl+parameter+key)
    else:
        # if urlopen immediately, INVALID_REQUEST response return.
        time.sleep(sleeptime)
        #print "url:",apiurl+nextpage+parameter+key
        response = urllib2.urlopen(apiurl+nextpage+parameter+key)
    jsonplace = json.loads(response.read())
    jsonlist = jsonplace['results']
    try:
        nextpage = 'pagetoken=' + jsonplace['next_page_token'] + '&'
    except Exception as e:
        print "=== Next page Not Found:", e.message 
        break

    for shop in jsonlist:
        keys = shop.keys()
        info = []
        db_session.add(Shop(shop["id"], shop["name"], "testtype", shop["geometry"]["location"]["lat"], shop["geometry"]["location"]["lng"]))
        db_session.commit()
    count += 1
print shopcount
