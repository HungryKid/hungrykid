from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import config.development as config

engine = create_engine(config.DATABASE_URI)

Session = scoped_session(sessionmaker(autocommit=False, autoflush=False,bind=engine))
db_session = Session()

app = Flask(__name__)
app.debug = True
app.secret_key = config.SECRET_KEY

import hungrykid.views
