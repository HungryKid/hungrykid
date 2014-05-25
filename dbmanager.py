from __init__ import engine
from user import metadata

# TODO if already created tables, drop it
metadata.create_all(engine)