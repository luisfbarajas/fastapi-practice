import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sqliteDBName = "../database.sqlite"
baseDir = os.path.dirname(os.path.realpath(__file__)) 

dataBaseURL = f"sqlite:///{os.path.join(baseDir,sqliteDBName)}"

engine =  create_engine(dataBaseURL,echo=True)

sesion = sessionmaker(bind=engine)

base = declarative_base()