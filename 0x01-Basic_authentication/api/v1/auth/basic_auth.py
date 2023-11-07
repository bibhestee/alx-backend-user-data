#!/usr/bin/env python3
"""
Basic Authentication Module
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
import binascii


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

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """
            decode base64 authorization header
            Arguments:
                base64_authorization_header
            Return:
                None if not base64 encoded
        """
        base64_auth_header = base64_authorization_header
        if not base64_auth_header or type(base64_auth_header) != str:
            return None
        try:
            decoded_base64_auth = b64decode(base64_auth_header)
            return decoded_base64_auth.decode('utf-8')
        except binascii.Error:
            return None
