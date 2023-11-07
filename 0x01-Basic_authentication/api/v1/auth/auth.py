#!/usr/bin/env python3
"""
Authentication module
"""
from flask import request
from typing import TypeVar, List


class Auth:
    """
        Auth - Authentication funtionality
        Methods:
            require_auth: check if path requires auth
            authorization_header: get auth header from path
            current_user: get the current user
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Require authentication method
            Arguments:
                path: endpoint path
                excluded_paths: endpoint paths that doesn't require auth
            Returns:
                False
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ Authorization header
            Arguments:
                request: flask request object
            Returns:
                None
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current user
            Arguments:
                request: flask request object
            Returns:
                None
        """
        return None
