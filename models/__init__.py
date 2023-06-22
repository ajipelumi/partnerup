#!/usr/bin/python3
""" Creates a unique database storage instance for our application. """
from models.engine.db_storage import DBStorage


# Create a unique FileStorage instance
storage = DBStorage()

# Reload the storage to load objects from database
storage.reload()
