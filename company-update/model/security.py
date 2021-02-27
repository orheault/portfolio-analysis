from sqlalchemy import Table, Column, String, Date, Integer, Float, Numeric, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .base import Base

class Security(Base):
    __tablename__ = 'security'
    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    description = Column(String)
    is_active = Column(Boolean)

    company_id = Column(Integer, ForeignKey('company.id'))
    company = relationship("Company", back_populates="securities")

    exchange_id = Column(Integer, ForeignKey('exchange.id'))
    exchange = relationship("Exchange")

    security_type_id = Column(Integer, ForeignKey('security_type.id'))
    security_type = relationship('SecurityType')

    def __init__(self, symbol, description=""):
        self.symbol = symbol
        self.description = description