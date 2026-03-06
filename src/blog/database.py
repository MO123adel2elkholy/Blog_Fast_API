from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

sqlalchemy_uri = 'sqlite:///.blog,db'

engin = create_engine(sqlalchemy_uri, connect_args={
                      'check_same_thread': False})

sessionlocal = sessionmaker(bind=engin, autocommit=False, autoflush=False)

Base = declarative_base()
