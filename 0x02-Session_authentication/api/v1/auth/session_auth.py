#!/usr/bin/env python3
""" 1. Empty session """
from .auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """this is the first creation"""
    user_id_by_session_id = {}
    def creat_session(self, user_id: str = None) -> str:
        """2. Create a session"""
        if user_id is None or not isinstance(user_id, str):
            return None
        id = uuid4()
        self.user_id_by_session_id[str(id)] = user_id
        return str(id)
