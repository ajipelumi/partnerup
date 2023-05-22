#!/usr/bin/python3
""" This module defines the class Partner. """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Partner(BaseModel, Base):
    """ This class defines a partner by various attributes. """
    __tablename__ = 'partners'
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    username = Column(String(128), nullable=False)
    email = Column(String(128), nullable=True)

    def __init__(self, *args, **kwargs):
        """ Initializes partner. """
        super().__init__(*args, **kwargs)