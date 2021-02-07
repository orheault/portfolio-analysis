# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://postgres:9604401@192.168.0.129:5432/portfolio')

Session = sessionmaker(bind=engine)

Base = declarative_base()