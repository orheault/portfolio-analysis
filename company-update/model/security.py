from sqlalchemy import Column, String, Date, Boolean, Integer, Float, ForeignKey
from .base import Base


class Security(Base):
    __tablename__ = 'security'
    symbol = Column(String, primary_key=True)
    description = Column(String)

    def __init__(self, symbol, description):
        self.symbol = symbol
        self.description = description