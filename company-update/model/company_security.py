from sqlalchemy import Table, Column, String, Date, Boolean, Integer, Float, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class CompanySecurity(Base):
    __tablename__ = 'company_security'
    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    description = Column(String)
    is_active = Column(Boolean)

    company_id = Column(Integer, ForeignKey('company.id'))
    company = relationship("Company", back_populates="company_securities")

    def __init__(self, symbol, description="", is_active=None, company_cik=None):
        self.symbol = symbol
        self.description = description
        self.is_active = is_active
        self.company_cik = company_cik