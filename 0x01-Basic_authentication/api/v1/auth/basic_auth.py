#!/usr/bin/env python3
"""
Basic Authentication Module
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
import binascii
from typing import TypeVar
from models.user import User
user = User()


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
        except UnicodeDecodeError:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """
            extract user credentials
            Arguments:
                decoded_base64_authorization_header
            Return:
                User email and password or None
        """
        if not decoded_base64_authorization_header:
            return (None, None)
        if type(decoded_base64_authorization_header) != str:
            return (None, None)
        if decoded_base64_authorization_header.find(':') == -1:
            return (None, None)
        details = decoded_base64_authorization_header.split(':', 1)
        return (details[0], details[1])

    def user_object_from_credentials(self, user_email: str, user_pwd:
                                     str) -> TypeVar('User'):
        """
            user object from credentials
            Arguments:
                user_email: user email address
                user_pwd: user password
            Return:
                User instance or None
        """
        if not user_email or type(user_email) != str:
            return None
        if not user_pwd or type(user_pwd) != str:
            return None
        user.load_from_file()
        users = user.all()
        if users != []:
            match_user = [user for user in users if user.email ==
                          user_email]
            # Check if user is in database
            if match_user == []:
                # Use the search method is no user in DB
                obj = user.search({'email': user_email})
                if obj != []:
                    # Validate password
                    if obj[0].is_valid_password(user_pwd):
                        return obj[0]
            else:
                # Validate password
                if match_user[0].is_valid_password(user_pwd):
                    return match_user[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
            current user
            Arguments:
                request: request method
            Return:
                the current user or None
        """
        if request:
            auth = self.authorization_header(request)
            if auth:
                token = self.extract_base64_authorization_header(auth)
                if token:
                    code = self.decode_base64_authorization_header(token)
                    if code:
                        user = self.extract_user_credentials(code)
                        if user:
                            out = self.user_object_from_credentials(user[0],
                                                                    user[1])
                            return out
        return None
