#!/usr/bin/python3
""" This module defines the class User. """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Table, Integer
from sqlalchemy.orm import relationship


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
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    username = Column(String(128), nullable=False)
    cohort_number = Column(Integer, nullable=False)
    partners = relationship('Partner', secondary=user_partner,
                            viewonly=False)

    def __init__(self, *args, **kwargs):
        """ Initializes user. """
        super().__init__(*args, **kwargs)
