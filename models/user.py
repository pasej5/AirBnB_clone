#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String


class User(BaseModel, Base):
    """
    Definition of the User class for the users table in
    the database.

    Attributes:
        __tablename__ : this represents "users".
        email : This represents a column (128 char), cant be null
        password : This represnts a column (128), cant be null
        first_name : This reprents a Column (128 char)
        can be null
        last_name : This represnts a column (128 char)
        can be null

    Args:
        BaseModel : the Basemodel class
        Base : declarative class
    """
    __tablename__ = 'users'

    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
