from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from .base import Base

class Exchange(Base):
    __tablename__ = 'exchange'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    EXCHANGE_TSX_ID =  6
    EXCHANGE_NASDAQ_ID = 7