from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.config.debug = True
app.config.from_object('hungrykid.config') # default
app.config.from_envvar('HUNGRYKID_CONFIG', silent=True) # production/development

engine = create_engine(app.config['DATABASE_URI'])

Session = scoped_session(sessionmaker(autocommit=False, autoflush=False,bind=engine))
db_session = Session()

import hungrykid.views
