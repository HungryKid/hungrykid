#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(root_dir, 'config'))

#import production as config
import development as config

from flask import Flask, render_template, redirect, request, session, url_for, Response, jsonify
import urllib
import urllib2
import json
from sqlalchemy.orm.exc import NoResultFound

from user import User
from shop import Shop
from __init__ import db_session

app = Flask(__name__)
app.secret_key = config.SECRET_KEY # TODO CHANGE THIS KEY(for Production Environment)

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
    shops = db_session.query(Shop)[0:10]
    shoplist = []
    for row in shops:
        # TODO: encoding
        shopdict = {}
        shopdict["id"] = row.id
        shopdict["name"] = row.name
        shopdict["type"] = row.type
        shopdict["lat"] = row.latitude
        shopdict["lng"] = row.longitude
        shoplist.append(shopdict)
    response = jsonify({'results' : shoplist})
    response.status_code = 200
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

if __name__ == '__main__':
    # If you enable debug support the server will reload itself on code changes
    # REMEMBER: You must not forget comment out below when deploy to production
    app.debug = True
    app.run()
