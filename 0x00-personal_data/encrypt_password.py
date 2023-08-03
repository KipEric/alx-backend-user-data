#!/usr/bin/env python3
"""
Module for hashing passwords using bcrypt
"""


import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes the password using bcrypt
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates if the provided password maches the hashed password
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
