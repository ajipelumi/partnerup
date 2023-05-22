#!/usr/bin/python3
""" Creates a unique database storage instance for our application. """
from models.engine.db_storage import DBStorage


storage = DBStorage()
storage.reload()
