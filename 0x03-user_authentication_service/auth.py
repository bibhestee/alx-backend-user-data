#!/usr/bin/env python3
"""
Authentication module
"""
import bcrypt


def _hash_password(password) -> bytes:
    """ hash password """
    salt = bcrypt.gensalt()
    pwd = password.encode()
    return bcrypt.hashpw(pwd, salt)
