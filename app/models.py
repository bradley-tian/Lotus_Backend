"""Database Models."""
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Numeric, Float, Boolean
from app import db

class Quotes(db.Model):
    __tablename__ = 'Quotes'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    ticker = Column(String)

    def __init__(self, data):
        for property, value in data.items():
            setattr(self, property, value)