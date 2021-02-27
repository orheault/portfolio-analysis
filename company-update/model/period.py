from .base import Base
from sqlalchemy import Column, String, Integer

class Period(Base):
    DAILY = 1

    __tablename__ = 'period'
    id = Column(Integer, primary_key=True)
    description = Column(String)
