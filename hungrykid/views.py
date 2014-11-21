#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

from hungrykid import app, db_session
from models.shop import Shop
from models.user import User

from flask import Flask, render_template, redirect, request, session, url_for, Response, jsonify, make_response
from sqlalchemy.orm.exc import NoResultFound
import urllib
import urllib2
import json
import random

FACEBOOK_APP_ID = app.config['FACEBOOK_APP_ID']
FACEBOOK_APP_SECRET = app.config['FACEBOOK_APP_SECRET']
FACEBOOK_URL = 'https://graph.facebook.com/'

@app.route('/')
def index():
    if session.get('access_token'):
        return redirect(url_for('settings'))
    else:
        return render_template('index.html')

@app.route('/settings')
def settings():
    if session.get('access_token'):
        return render_template('settings.html', user=getUserFromFB())
    else:
        return redirect(url_for('index'))

def getUserFromFB():
    response = urllib2.urlopen(FACEBOOK_URL + 'me?' + session.get('access_token'))
    user_json = json.loads(response.read())
    id = user_json["id"]
    try:
        user = db_session.query(User).filter(User.uid == id).one()
    except NoResultFound:
        # TODO Use transaction
        db_session.add(User(id, user_json["name"]))
        db_session.commit()

    return user_json

###### API ######
@app.route('/api/getshoplist')
def getshoplist():
    typequery = request.args.get('type', '')
    # TODO if number of shops is enormous, this implements use enough memory
    if typequery:
        shops = db_session.query(Shop).filter(Shop.type == typequery)
    else:
        shops = db_session.query(Shop)
    shoplist = []
    for row in shops:
        shoplist.append({"id": row.shopid, "name": row.name, "type": row.type, "lat": row.latitude, "lng": row.longitude, "weight": row.weight})

    shopcount = len(shoplist)
    recommend = []
    for num in range(10):
        while True:
          picknum = random.randint(0, shopcount-1)
          val = random.randint(0, 10)
          if shoplist[picknum]["weight"] > val:
            break
        recommend.append(shoplist.pop(picknum))
        shopcount -= 1

    shopjson = json.dumps({'results' : recommend}, ensure_ascii=False, indent=2)
    response = make_response(shopjson)
    response.status_code = 200
    response.headers['Content-type'] = "application/json; charset='utf-8'"
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response

##### LOGIN/OUT #####
@app.route('/login')
def login():
    code = request.args.get('code')
    uri = request.url_root + 'login'
    args = dict(client_id=FACEBOOK_APP_ID, redirect_uri=uri)
    if code is None:
        return redirect(FACEBOOK_URL + "oauth/authorize?" + urllib.urlencode(args))
    args["client_secret"] = FACEBOOK_APP_SECRET
    args["code"] = code
    response = urllib.urlopen(FACEBOOK_URL + "oauth/access_token?" + urllib.urlencode(args))
    session['access_token'] = response.read()
    return redirect(url_for('settings'))

@app.route('/logout')
def logout():
    session.pop('access_token', None)
    session.pop('userinfo', None)
    return redirect(url_for('index'))

###### ERROR HANDLER #####
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500
