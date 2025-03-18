from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

produccionDB = create_engine('sqlite:///produccionDB.sqlite')
testDB = create_engine('sqlite:///testDB.sqlite')
Session = sessionmaker(bind=testDB)

Base = declarative_base()
session = Session()
