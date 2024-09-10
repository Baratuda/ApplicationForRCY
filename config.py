import os
from sqlalchemy import create_engine

basedir = os.path.abspath(os.path.dirname(__file__))
engine = create_engine('sqlite:///' + os.path.join(basedir, 'myDB.db'))

