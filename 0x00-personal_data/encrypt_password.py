#!/usr/bin/env python3
"""encrypting password"""
import bcrypt


def hash_password(password: str) -> bytes:
    """encrypting password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ checck valid password """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

if __name__ == "__main__":
    main()
