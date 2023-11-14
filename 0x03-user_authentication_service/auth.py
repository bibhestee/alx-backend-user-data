#!/usr/bin/env python3
"""
Authentication module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ hash password """
    salt = bcrypt.gensalt()
    pwd = password.encode()
    return bcrypt.hashpw(pwd, salt)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ register user
            Arguments:
                email(required): email address of the user
                password(required): password of the user
            Return:
                user
        """
        # check if user exists
        try:
            user_exists = self._db.find_user_by(email=email)
            if user_exists:
                message = 'User {} already exists'.format(email)
                raise ValueError(message)
        except NoResultFound:
            hsh_pwd = _hash_password(password)
            user = self._db.add_user(email, hsh_pwd)
            return user
