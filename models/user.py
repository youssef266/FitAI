#!/use/bin/python3
"""
class user
"""

from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker
from models.base_model import BaseModel, Base


class Users(BaseModel, Base):
    __tablename__ = 'users'

    name = Column(String(80), nullable=False)
    email = Column(String(80), nullable=False)
    password = Column(String(80), nullable=False)
    conf_password = Column(String(80), nullable=False)
    age = Column(String(80), nullable=False)
    gender = Column(String(80), nullable=False)
    weight = Column(String(80), nullable=False)
    height = Column(String(80), nullable=False)

engine = create_engine("sqlite:///youssef.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
