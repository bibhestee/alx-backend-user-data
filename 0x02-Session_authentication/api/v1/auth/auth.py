#!/usr/bin/env python3
"""
Authentication module
"""
from flask import request
from typing import TypeVar, List
import re
from os import getenv


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
                False if path requires auth or True otherwise
        """
        if not path:
            return True
        if not excluded_paths or excluded_paths == []:
            return True
        # Check if path ends with slash
        if path[-1] == '/' and path in excluded_paths:
            return False
        elif path+'/' in excluded_paths:
            return False
        else:
            pattern = r'\/api\/v1\/(\w+)'
            star_urls = [url for url in excluded_paths if url[-1] == '*']
            if star_urls != []:
                for url in star_urls:
                    url_end = re.match(pattern, url)
                    path_end = re.match(pattern, path)
                    if re.match(url_end.group(1), path_end.group(1)):
                        return False
            return True

    def authorization_header(self, request=None) -> str:
        """ Authorization header
            Arguments:
                request: flask request object
            Returns:
                Authorization header value or None
        """
        if not request:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current user
            Arguments:
                request: flask request object
            Returns:
                None
        """
        return None

    def session_cookie(self, request=None) -> str:
        """ Session cookie
            Arguments:
               request: flask request object
            Returns:
                None or Cookie value
        """
        if not request:
            return None
        cookie_name = getenv('SESSION_NAME')
        return request.cookies.get(cookie_name)
