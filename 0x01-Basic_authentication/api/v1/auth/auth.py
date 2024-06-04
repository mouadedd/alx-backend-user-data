#!/usr/bin/env python3
"""3. Auth class"""
from flask import request
from typing import List, TypeVar

class Auth():
    """template for all authentication system you will implement"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns False - path and excluded_paths"""
        
        if path is None:
            return True
        elif excluded_paths is None or len(excluded_paths) == 0:
            return True
        elif path in excluded_paths:
            return False
        else:
            for elem in excluded_paths:
                if elem.startswith(path) or path.startswith(elem):
                    return False
                if elem.endswith("*") and path.startswith(elem[:-1]):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """returns None - request will be the Flask request object"""
        if request is None:
            return None
        header = request.headers.get('Authorization')
        return header if header else None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None - request will be the Flask request object"""
        return None