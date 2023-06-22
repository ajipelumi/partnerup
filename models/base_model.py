#!/usr/bin/python3
""" Base of all classes. """
from datetime import datetime
import models
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid


# Set the format for datetime
time = "%Y-%b-%d %H:%M"

# Create the base class for declarative SQLAlchemy models
Base = declarative_base()


class BaseModel():
    """ Defines all base attributes/methods for all classes."""
    # Define the id attribute
    id = Column(String(60), primary_key=True)
    # Define the created_at attribute
    created_at = Column(DateTime, default=datetime.utcnow)
    # Define the updated_at attribute
    updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """ Initialization of the base model. """
        # Check if kwargs is not empty
        if kwargs:
            # Loop through kwargs
            for key, value in kwargs.items():
                # Check if key is not __class__
                if key != "__class__":
                    # Set the key/value pair as an attribute
                    setattr(self, key, value)

            # Check if created_at exists and is a string
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                # Convert string to datetime object
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
                # Set created_at to current datetime if it doesn't exist
                self.created_at = datetime.utcnow()

            # Check if updated_at exists and is a string
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                # Convert string to datetime object
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                # Set updated_at to current datetime if it doesn't exist
                self.updated_at = datetime.utcnow()

            # Check if id exists
            if kwargs.get("id", None) is None:
                # Set id to a unique string
                self.id = str(uuid.uuid4())
        else:
            # Set id to a unique string if kwargs is empty
            self.id = str(uuid.uuid4())
            # Set created_at to current datetime
            self.created_at = datetime.utcnow()
            # Set updated_at to current datetime
            self.updated_at = self.created_at

    def __str__(self):
        """ Returns a string representation. """
        # Return a string representation of the object
        return f'[{self.__class__.__name__}] ({self.id}) {self.__dict__}'

    def save(self):
        """
        Updates the public instance attribute updated_at
        with the current datetime.
        """
        # Update updated_at with current datetime
        self.updated_at = datetime.now()
        # Add the current instance to the models.storage
        models.storage.new(self)
        # Save changes to the database
        models.storage.save()

    def to_dict(self):
        """ Returns a dictionary containing all keys/values of __dict__. """
        # Create a copy of __dict__
        new_dict = self.__dict__.copy()

        # Convert created_at to string if it exists
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)

        # Convert updated_at to string if it exists
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)

        # Add the class name to the dictionary
        new_dict["__class__"] = self.__class__.__name__

        # Remove the key _sa_instance_state from the dictionary
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]

        # Return the new dictionary
        return new_dict

    def delete(self):
        """ Delete the current instance from the models.storage. """
        # Delete the current instance from the models.storage
        models.storage.delete(self)
