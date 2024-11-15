import os
from sqlalchemy import create_engine

basedir = os.path.abspath(os.path.dirname(__file__))
engine = create_engine('sqlite:///' + os.path.join(basedir, 'myDB.db'))
DEBUG = True
TEMPLATES_AUTO_RELOAD = True
SECRET_KEY = '12345'
DEBUG_TB_INTERCEPT_REDIRECTS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'myDB.db')
CACHE_TYPE = "SimpleCache"
CACHE_DEFAULT_TIMEOUT = 300

