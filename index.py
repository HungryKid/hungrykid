from flask import Flask, render_template, redirect, request, session, url_for
import urllib
import urllib2
import json
from sqlalchemy import create_engine,
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from user import User

engine = create_engine('mysql+pymysql://hungry:imhungry@localhost/sandwich', encoding='utf-8')

Session = scoped_session(sessionmaker(autocommit=False, autoflush=False,bind=engine))
sessions = Session()

app = Flask(__name__)
app.secret_key = "INSERT HERE"

FACEBOOK_APP_ID = "INSERT HERE"
FACEBOOK_APP_SECRET = "INSERT HERE"
SITE_URL = "http://sandwich.com:5000/"

@app.route('/')
def index():
    access_token = session.get('access_token')
    if not access_token is None:
        getUserFromFB()
    
    return render_template('index.html')

@app.route('/help')
def help():
    return 'This is help page'

@app.route('/user/<username>')
def userpage(username):
    #return 'This is %s\'s page ' % username
    return render_template('userpage.html')


def getUserFromFB():
    response = urllib2.urlopen('https://graph.facebook.com/me?' + session.get('access_token'))
    user_json = json.loads(response.read())

    try:
        user = sessions.query(User).filter(User.id == user_json["id"]).one()
    except NoResultFound:
        print "NOUSER"
        # TODO create user in DB 

    session['userinfo'] = user_json # TODO use mysql?


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


###### ERROR HANDLER
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
