#!/usr/bin/env python3
"""
encrpyt password module
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ hash password into bytes """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ check if password is valid and equal to hashed password """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
