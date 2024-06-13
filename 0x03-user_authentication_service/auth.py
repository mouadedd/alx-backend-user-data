#!/usr/bin/env python3
""" 4 -hash password """
import bcrypt
from db import DB, User
from typing import Union
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """ 4. Hash password """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """9. Generate UUIDs
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Register user
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        else:
            raise ValueError("User %s already exists" % email)

    def valid_login(self, email: str, password: str) -> bool:
        """
        8. Credentials validation
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode(), user.hashed_password)

    def create_session(self, email: str) -> Union[str, None]:
        """10. Get session ID
        """
        session_id = _generate_uuid()
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            pass
        else:
            try:
                self._db.update_user(user.id, session_id=session_id)
            except (NoResultFound, ValueError):
                pass
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """ 12 Find user by session ID
        """
        if session_id is not None:
            try:
                user = self._db.find_user_by(session_id=session_id)
                return user
            except NoResultFound:
                pass
        return None

    def destroy_session(self, user_id: str) -> None:
        """13. Destroy session
        """
        return self._db.update_user(user_id, session_id=None)
