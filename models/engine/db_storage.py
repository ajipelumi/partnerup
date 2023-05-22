#!/usr/bin/python3
""" This module defines a class to manage database storage for partnerup. """
import models
from models.base_model import Base
from models.partner import Partner
from models.user import User
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session

classes = {"User": User, "Partner": Partner}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        PARTNERUP_MYSQL_USER = getenv('PARTNERUP_MYSQL_USER')
        PARTNERUP_MYSQL_PWD = getenv('PARTNERUP_MYSQL_PWD')
        PARTNERUP_MYSQL_HOST = getenv('PARTNERUP_MYSQL_HOST')
        PARTNERUP_MYSQL_DB = getenv('PARTNERUP_MYSQL_DB')
        PARTNERUP_ENV = getenv('PARTNERUP_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(PARTNERUP_MYSQL_USER,
                                             PARTNERUP_MYSQL_PWD,
                                             PARTNERUP_MYSQL_HOST,
                                             PARTNERUP_MYSQL_DB))
        if PARTNERUP_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Returns a dictionary of models currently in database storage. """
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """ Add the object to the current database session. """
        self.__session.add(obj)

    def save(self):
        """ Commit all changes of the current database session. """
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete from the current database session. """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """ Reloads data from the database. """
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session)
        self.__session = Session()

    def close(self):
        """ Calls the remove method. """
        self.__session.close()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found.
        """
        if cls not in classes.values():
            return None
        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if (value.id == id):
                return value
        return None

    def count(self, cls=None):
        """
        Count the number of objects in storage.
        """
        all_class = classes.values()
        if not cls:
            count = 0
            for clas in all_class:
                count += len(models.storage.all(clas).values())
        else:
            count = len(models.storage.all(cls).values())
        return count