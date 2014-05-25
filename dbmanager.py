from __init__ import engine
from user import metadata, users

users.drop(engine)
metadata.create_all(engine)