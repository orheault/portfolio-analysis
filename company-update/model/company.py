from .base import Base
from sqlalchemy import Table, Column, String, Numeric, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship



class Company(Base):
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True)
    description = Column(String)
    name = Column(String)
    is_active = Column(Boolean)
    sector_id = Column(Integer)
    industry_id = Column(Integer)
    
    securities = relationship("Security", back_populates="company")

    def __init__(self, description = "", is_active = True, name="", industry_id=1, sector_id=1):
        self.description = description
        self.is_active = is_active
        self.name = name
        self.industry_id = industry_id
        self.sector_id = sector_id
