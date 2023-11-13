#!/usr/bin/env python3
"""
User model module
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()


class User(Base):
    """
        User - User class
        Methods:
            None
        Attributes:
            id: user id
            name: user name
            email: user email
            hashed_password: hashed password of the user
            session_id: user session id
            reset_token: reset token key
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    session_id = Column(String, nullable=False)
    reset_token = Column(String, nullable=False)
