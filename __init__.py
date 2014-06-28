from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('mysql+pymysql://root@localhost/sandwich?charset=utf8')

Session = scoped_session(sessionmaker(autocommit=False, autoflush=False,bind=engine))
db_session = Session()
