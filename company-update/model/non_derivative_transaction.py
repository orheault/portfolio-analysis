from sqlalchemy import Column, String, Date, Boolean, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship, backref
from .base import Base

class NonDerivativeTransaction(Base):
    __tablename__ = 'non_derivative_transaction'
    id = Column(Integer, primary_key=True)
    amount_share = Column(String)
    price_per_share = Column(Float)
    transaction_code = Column(String)
    
    security_type_id = Column(Integer, ForeignKey('security_type.id'))
    security_type = relationship("SecurityType") # , backref=backref("security_type", uselist=False)

    inside_trader_id = Column(Integer, ForeignKey('inside_trader.id'))
    inside_trader = relationship("InsideTrader") # , backref=backref("inside_trader", uselist=False)
    

    def __init__(self, amount_share, price_per_share, transaction_code, security_type):
        self.amount_share = amount_share
        self.price_per_share = price_per_share
        self.transaction_code = transaction_code
        self.security_type= security_type

    def add_inside_trader(self, inside_trader):
        self.inside_trader = inside_trader