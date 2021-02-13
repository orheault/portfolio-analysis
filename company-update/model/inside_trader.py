from .base import Base
from sqlalchemy import Column, String, Date, Boolean, Integer
from sqlalchemy.orm import relationship


class InsideTrader(Base):
    __tablename__ = 'inside_trader'
    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    reporting_owner_name = Column(String)
    transaction_date = Column(Date)
    reporting_owner_relationship_is_director = Column(Boolean)
    reporting_owner_relationship_is_officer  = Column(Boolean)
    reporting_owner_relationship_is_ten_percent  = Column(Boolean)
    reporting_owner_relationship_is_other= Column(Boolean)
    reporting_owner_relationship_description = Column(String)

    non_derivative_transactions = relationship("NonDerivativeTransaction", back_populates = "inside_trader")

    def __init__(self, symbol, reporting_owner_name, transaction_date, reporting_owner_relationship_is_director, reporting_owner_relationship_is_officer, reporting_owner_relationship_is_ten_percent, reporting_owner_relationship_is_other, reporting_owner_relationship_description):
        self.symbol = symbol
        self.reporting_owner_name = reporting_owner_name
        self.transaction_date = transaction_date
        self.reporting_owner_relationship_is_director = reporting_owner_relationship_is_director
        self.reporting_owner_relationship_is_officer = reporting_owner_relationship_is_officer
        self.reporting_owner_relationship_is_ten_percent = reporting_owner_relationship_is_ten_percent
        self.reporting_owner_relationship_is_other = reporting_owner_relationship_is_other
        self.reporting_owner_relationship_description = reporting_owner_relationship_description
    