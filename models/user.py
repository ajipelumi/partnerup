#!/usr/bin/python3
""" This module defines the class User. """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """ This class defines a user by various attributes. """
    __tablename__ = 'users'
    email = Column(String(128), nullable=True)
    password = Column(String(128), nullable=False)
    username = Column(String(128), nullable=False)
    partners = relationship('Partner', cascade='all, delete',
                            backref='user')
    
    def __init__(self, *args, **kwargs):
        """ Initializes user. """
        super().__init__(*args, **kwargs)