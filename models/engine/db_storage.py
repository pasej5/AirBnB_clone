#!/usr/bin/python3
"""This module defines the DBStorage class for AirBnB project"""

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models import base_model, user, state, city, amenity, place, review


class DBStorage:
    """This class manages the database storage for AirBnB project"""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize DBStorage instance"""
        db_user = getenv("HBNB_MYSQL_USER")
        db_pwd = getenv("HBNB_MYSQL_PWD")
        db = getenv("HBNB_MYSQL_DB")
        db_host = getenv("HBNB_MYSQL_HOST")
        environment = getenv("HBNB_ENV")
        connection_url = f"mysql+mysql://{db_user}:{db_pwd}@{db_host}/db"

        self.__engine = create_engine(connection_url, pool_pre_ping=True)

        if environment == 'test':
            metadata.drop_all(bind=self._engine)

    def all(self, cls=None):
        """Query all objects depending on class name"""
        from models import base_model, user, state, city, amenity, place, review

        session = self.__session
        objects = {}

        if cls is None:
            classes = [base_model.BaseModel, user.User, state.State, city.City,
                       amenity.Amenity, place.Place, review.Review]
        else:
            classes = [cls]

        for c in classes:
            for obj in session.query(c).all():
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                objects[key] = obj

        return objects

    def new(self, obj):
        """Add the object to the current database session"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables and create a session"""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                                      expire_on_commit=False))
