#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import config.development as config

from hungrykid import app, db_session
from models.shop import Shop
from models.user import User

from flask import Flask, render_template, redirect, request, session, url_for, Response, jsonify, make_response
import urllib
import urllib2
import json
from sqlalchemy.orm.exc import NoResultFound

FACEBOOK_APP_ID = config.FACEBOOK_APP_ID
FACEBOOK_APP_SECRET = config.FACEBOOK_APP_SECRET

SITE_URL = config.SITE_URL

@app.route('/')
def index():
    access_token = session.get('access_token')
    user = None
    if not access_token is None:
        user = getUserFromFB()
    
    return render_template('index.html', user=user)

# TODO
@app.route('/help')
def help():
    return 'This is help page'

# TODO
@app.route('/user/<username>')
def userpage(username):
    return render_template('userpage.html')

def getUserFromFB():
    response = urllib2.urlopen('https://graph.facebook.com/me?' + session.get('access_token'))
    user_json = json.loads(response.read())
    id = user_json["id"]
    try:
        user = db_session.query(User).filter(User.id == id).one()
    except NoResultFound:
        # TODO Use transaction
        db_session.add(User(id, user_json["name"]))
        db_session.commit()

    return user_json

###### API ######
@app.route('/api/getshoplist')
def getshoplist():
    typequery = request.args.get('type', '')
    if typequery:
        shops = db_session.query(Shop).filter(Shop.type == typequery)
    else:
        shops = db_session.query(Shop)[0:10]
    shoplist = []
    for row in shops:
        shopdict = {}
        shopdict["id"] = row.id
        shopdict["name"] = row.name
        shopdict["type"] = row.type
        shopdict["lat"] = row.latitude
        shopdict["lng"] = row.longitude
        shoplist.append(shopdict)
    shopjson = json.dumps({'results' : shoplist}, ensure_ascii=False, indent=2)
    response = make_response(shopjson)
    response.status_code = 200
    response.headers['Content-type'] = "application/json; charset='utf-8'"
    return response

##### LOGIN/OUT #####
@app.route('/login')
def login():
    code = request.args.get('code')
    args = dict(client_id=FACEBOOK_APP_ID, redirect_uri=SITE_URL+"login")
    if code is None:
        return redirect("https://graph.facebook.com/oauth/authorize?" + urllib.urlencode(args))
    args["client_secret"] = FACEBOOK_APP_SECRET
    args["code"] = code
    response = urllib.urlopen("https://graph.facebook.com/oauth/access_token?" + urllib.urlencode(args))
    print "res:", response
    session['access_token'] = response.read()
    return redirect(SITE_URL)


@app.route('/logout')
def logout():
    session.pop('access_token', None)
    session.pop('userinfo', None)
    #flash('You were logged out')
    return redirect(url_for('index'))


###### ERROR HANDLER #####
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500