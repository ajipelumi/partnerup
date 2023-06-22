#!/usr/bin/python3
""" This module defines a class to manage database storage for partnerup. """
import models
from models.base_model import Base
from models.partner import Partner
from models.user import User
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# Create a dictionary of classes
classes = {"User": User, "Partner": Partner}


class DBStorage:
    """interaacts with the MySQL database"""
    # Create class attributes
    __engine = None
    __session = None

    def __init__(self):
        """ Instantiate a DBStorage object. """
        # Get environment variables
        PARTNERUP_MYSQL_USER = getenv('PARTNERUP_MYSQL_USER')
        PARTNERUP_MYSQL_PWD = getenv('PARTNERUP_MYSQL_PWD')
        PARTNERUP_MYSQL_HOST = getenv('PARTNERUP_MYSQL_HOST')
        PARTNERUP_MYSQL_DB = getenv('PARTNERUP_MYSQL_DB')
        PARTNERUP_ENV = getenv('PARTNERUP_ENV')

        # Create an engine that connects to the MySQL server
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(PARTNERUP_MYSQL_USER,
                                             PARTNERUP_MYSQL_PWD,
                                             PARTNERUP_MYSQL_HOST,
                                             PARTNERUP_MYSQL_DB))

        # Drop all tables if the environment is test
        if PARTNERUP_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Returns a dictionary of models currently in database storage. """
        # Create a new dictionary
        new_dict = {}

        # Iterate through all classes in the dictionary of classes
        for clss in classes:

            # If the class is None or the class is the same as the class
            if cls is None or cls is classes[clss] or cls is clss:

                # Query the current database session for all class objects
                objs = self.__session.query(classes[clss]).all()

                # Iterate through the list of objects
                for obj in objs:

                    # Create a key for the object
                    key = obj.__class__.__name__ + '.' + obj.id

                    # Set the value of the key to the object
                    new_dict[key] = obj

        # Return the new dictionary
        return (new_dict)

    def new(self, obj):
        """ Add the object to the current database session. """
        # Add the object to the current database session
        self.__session.add(obj)

    def save(self):
        """ Commit all changes of the current database session. """
        # Commit all changes of the current database session
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete from the current database session. """
        # Delete from the current database session if the object is not None
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """ Reloads data from the database. """
        # Create all tables in the database
        Base.metadata.create_all(self.__engine)

        # Create a new session to interact with the database
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)

        # Create a scoped session to ensure different users' interactions
        Session = scoped_session(session)

        # Create the current database session
        self.__session = Session()

    def close(self):
        """ Calls the remove method. """
        # Close the current database session
        self.__session.close()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found.
        """
        # Return None if the class is not in the dictionary of classes
        if cls not in classes.values():
            return None

        # Get all objects of the class
        all_cls = models.storage.all(cls)

        # Iterate through the objects of the class
        for value in all_cls.values():

            # Return the object if the ID matches
            if (value.id == id):
                return value

        # Return None if the ID does not match
        return None

    def count(self, cls=None):
        """
        Count the number of objects in storage.
        """
        # Get all classes in the dictionary of classes
        all_class = classes.values()

        # Check if class is None
        if not cls:
            count = 0
            # Iterate through all classes
            for clas in all_class:
                # Add the number of objects of the class to the count
                count += len(models.storage.all(clas).values())
        else:
            # Add the number of objects of the class to the count
            count = len(models.storage.all(cls).values())

        # Return the count
        return count
