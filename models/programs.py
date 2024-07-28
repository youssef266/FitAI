#!/usr/bin/python3
"""
programs class
"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker


class Programs(BaseModel, Base):
    __tablename__ = 'programs'

    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    program_text = Column(String(1024), nullable=True)

engine = create_engine("sqlite:///youssef.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
