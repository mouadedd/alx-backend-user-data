#!/usr/bin/env python3
""" 4 -hash password """
import bcrypt
from db import DB, User


def _hash_password(password: str) -> bytes:
    """ 4. Hash password """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
