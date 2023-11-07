#!/usr/bin/env python3
"""
Basic Authentication Module
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
        BasicAuth - Basic Authentication Class
    """
    def extract_base64_authorization_header(self, authorization_header:
                                            str) -> str:
        """
            extract base64 auth header
            Arguments:
                authorization_header: authorization header
            Return:
                None
        """
        auth = authorization_header
        if not auth or type(auth) != str or not auth.startswith('Basic '):
            return None
        return auth.split(' ')[1]
