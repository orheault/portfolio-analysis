from sqlalchemy import Column, String, Date, Boolean, Integer, Float, ForeignKey
from dao.base import Base
from dao.base import db

class Security(db.Model):
    id = db.Column(db.String, primary_key=True)
    description = db.Column(db.String)

    def __init__(self, symbol, description):
        self.symbol = symbol
        self.description = description