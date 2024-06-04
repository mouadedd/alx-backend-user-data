#!/usr/bin/env python3
"""6. Basic auth"""
import base64
from .auth import Auth
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """this is a test"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """returns the Base64 part of the 
        Authorization header for a Basic Authentication"""
        if authorization_header is None or not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        value = authorization_header.split(" ")[-1]
        return value
    
    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """returns the decoded value of a Base64 string"""
        if base64_authorization_header is None or not isinstance(base64_authorization_header, str):
            return None
        try:
            deco = base64_authorization_header.encode('utf-8')
            deco = base64.b64decode(deco)
            return deco.decode('utf-8')
        except Exception:
            return None
    
    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """returns the user email and password from the Base64 decoded value.
        """
        if decoded_base64_authorization_header is None or not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        e_mail = decoded_base64_authorization_header.split(':')[0]
        pswd = decoded_base64_authorization_header[len(e_mail) + 1:]
        return (e_mail, pswd)
    
    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """returns the User instance based on his email and password."""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
            if not users or len(users) == 0:
                return None
            for memb in users:
                if memb.is_valid_password(user_pwd):
                    return memb
            return None
        except Exception:
            return None
    
    def current_user(self, request=None) -> TypeVar('User'):
        """overloads Auth and retrieves the User instance for a request"""
        auth_header = self.authorization_header(request)
        if auth_header is not None:
            tok = self.extract_base64_authorization_header(auth_header)
            if tok is not None:
                deco = self.decode_base64_authorization_header(tok)
                if deco is not None:
                    e_mail, pswd = self.extract_user_credentials(deco)
                    if e_mail is not None:
                        return self.user_object_from_credentials(e_mail, pswd)
        return