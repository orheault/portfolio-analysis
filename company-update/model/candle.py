from .base import Base
from sqlalchemy import Table, Column, String, Numeric, Boolean, ForeignKey, Integer, TIMESTAMP, UniqueConstraint
from sqlalchemy.orm import relationship

class Candle(Base):
    __tablename__ = 'candle'
    
    id = Column(Integer, primary_key=True)

    high = Column(Numeric)
    low = Column(Numeric)
    open = Column(Numeric)
    close = Column(Numeric)
    date_ = Column(TIMESTAMP)
    volume = Column(Integer)

    security_id = Column(Integer, ForeignKey('security.id'))
    period_id = Column(Integer, ForeignKey('period.id'))
    
    def __init__(self, high, low, open, close, volume, start, period_id, security_id):
        self.high = high
        self.low = low
        self.open = open
        self.close = close
        self.volume = volume
        self.security_id = security_id
        self.period_id = period_id
        self.date_ = start

        