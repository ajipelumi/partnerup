#!/usr/bin/python3
""" This module defines the class Partner. """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String


class Partner(BaseModel, Base):
    """ This class defines a partner by various attributes. """
    __tablename__ = 'partners'
    username = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)

    def __init__(self, *args, **kwargs):
        """ Initializes partner. """
        super().__init__(*args, **kwargs)
