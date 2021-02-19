from .base import Base
from sqlalchemy import Table, Column, String, Numeric, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship



class Company(Base):
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True)
    cik = Column(Numeric)
    description = Column(String)
    is_active = Column(Boolean)
    
    company_securities = relationship("CompanySecurity", back_populates="company")

    def __init__(self, cik, description = "", is_active = True):
        self.cik = cik
        self.description = description
        self.is_active = is_active
