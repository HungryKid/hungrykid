#!/usr/bin/env python
# coding:utf-8
#
# google place api crawler
#
import urllib2
import json
import time
import codecs
from hungrykid import app
from hungrykid import db_session
from hungrykid.models.shop import Shop

from sqlalchemy import create_engine, Table, MetaData, Column, types
from sqlalchemy.orm import scoped_session, sessionmaker, mapper
from sqlalchemy.orm.exc import NoResultFound

import random

KEYWORDLIST_PATH = 'keyword.txt'
# 1loop can get 20shops. 20x3loop=60shops are google place api restriction 
LOOPNUM = 3 
SLEEPSEC = 3

apiurl = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
parameter = 'location=35.6571942,139.7093825&radius=500&types=restaurant&sensor=false&keyword='
key = "key=" + app.config['GOOGLE_API_KEY']

photoapiurl = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&'
photoparameter = '&sensor=false&photoreference='

detailapiurl = 'https://maps.googleapis.com/maps/api/place/details/json?reference='
detailparameter = '&sensor=true&'

def getFoodWithCategory(url, category):
  count = 0
  shopcount = 0
  nextpage = None
  while count < LOOPNUM:
    if nextpage is None:
      response = urllib2.urlopen(url)
    else:
      # if urlopen immediately, INVALID_REQUEST response return.
      time.sleep(SLEEPSEC)
      response = urllib2.urlopen(url)
    jsonplace = json.loads(response.read())
    jsonlist = jsonplace['results']
    for shop in jsonlist:
      keys = shop.keys()
      info = []
      try:
        db_session.query(Shop).filter(Shop.shopid == shop["id"]).one()
      except NoResultFound:
        # if target shop is not already exist, register it
        addShop(shop,category)
      except:
        # TODO
        print "Unexpected error"
      shopcount += 1
  
    try:
      nextpage = 'pagetoken=' + jsonplace['next_page_token'] + '&'
    except Exception as e:
      #print "= Next page Not Found:", e.message 
      break
    count += 1
  print category, ":", shopcount, "shops found"

# Add shop information with detail and photo api
def addShop(shop,category):
  detailreference = shop["reference"]
  detailurl= detailapiurl+detailreference+detailparameter+key
  response = urllib2.urlopen(detailurl)
  jsondetail = json.loads(response.read())
  shopdetail = jsondetail["result"]
  url = shopdetail["url"]
  try:
    phone = shopdetail["formatted_phone_number"]
  except:
    phone = ""

  try:
    photoreference = shop["photos"][0]["photo_reference"]
    photourl = photoapiurl+key+photoparameter+photoreference
  # if photo isn't exist, emit KeyError
  except KeyError:
    photourl = ""
#  if photourl is not None:
  db_session.add(Shop(shop["id"], shop["name"], category,
                 shop["geometry"]["location"]["lat"],
                 shop["geometry"]["location"]["lng"],
                 photourl, random.randint(0, 10), url, phone))
  db_session.commit()

kwlist = codecs.open(KEYWORDLIST_PATH, "r", "utf-8")

for kw in kwlist:
  kw = kw.rstrip()
  encodedkw = urllib2.quote(kw.encode("utf-8")) + "&"
  getFoodWithCategory(apiurl+parameter+encodedkw+key, kw)
