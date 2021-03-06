from sqlalchemy import Column, String, Date, Boolean, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class SecurityType(Base):
    __tablename__ = 'security_type'
    id = Column(Integer, primary_key=True)
    title = Column(String)

    #non_derivative_transactions = relationship("NonDerivativeTransaction", back_populates = "security_type")

    SECURITY_TYPE_COMMON_STOCK = 1
    SECURITY_TYPE_EXCHANGE_TRADED_FUND = 2


    def __init__(self,title):
        self.title = title

    def __init__(self, id, title):
        self.id = id
        self.title = title