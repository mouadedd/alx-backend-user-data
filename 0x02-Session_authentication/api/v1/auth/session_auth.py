#!/usr/bin/env python3
""" 1. Empty session """
from .auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """this is the first creation"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """2. Create a session"""
        if user_id is None or not isinstance(user_id, str):
            return None
        id = uuid4()
        self.user_id_by_session_id[str(id)] = user_id
        return str(id)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """3. User ID for Session ID"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)
    
    def current_user(self, request=None):
        """6. Use Session ID for identifying a User"""
        sess_cookie = self.session_cookie(request)
        u_id = self.user_id_for_session_id(sess_cookie)
        user =  User.get(u_id)
        return user
