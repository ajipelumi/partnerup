#!/usr/bin/python3
""" This module defines the class Partner. """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer


class Partner(BaseModel, Base):
    """ This class defines a partner by various attributes. """
    # Set the name of the table in which the database will store partners
    __tablename__ = 'partners'

    # Initialize partner attributes
    username = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    cohort_number = Column(Integer, nullable=False)

    def __init__(self, *args, **kwargs):
        """ Initializes partner. """
        # Call the super class constructor
        super().__init__(*args, **kwargs)
