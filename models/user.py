#!/usr/bin/python3
""" This module defines the class User. """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Table, Integer
from sqlalchemy.orm import relationship


# Create a many-to-many relationship between users and partners
user_partner = Table('user_partner', Base.metadata,
                     Column('user_id', String(60),
                            ForeignKey('users.id', onupdate='CASCADE',
                                       ondelete='CASCADE'),
                            primary_key=True),
                     Column('partner_id', String(60),
                            ForeignKey('partners.id', onupdate='CASCADE',
                                       ondelete='CASCADE'),
                            primary_key=True))


class User(BaseModel, Base):
    """ This class defines a user by various attributes. """
    # Set the name of the table in which the database will store users
    __tablename__ = 'users'

    # Initialize user attributes
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    username = Column(String(128), nullable=False)
    cohort_number = Column(Integer, nullable=False)

    # Define the relationship between users and partners
    partners = relationship('Partner', secondary=user_partner,
                            viewonly=False)

    def __init__(self, *args, **kwargs):
        """ Initializes user. """
        # Call the super class constructor
        super().__init__(*args, **kwargs)
