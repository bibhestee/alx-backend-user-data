#!/usr/bin/env python3
"""
    Session Authentication Expiration Module
"""
from api.v1.auth.session_auth import SessionAuth
from uuid import uuid4
from os import getenv
from models.user import User
from datetime import timedelta, datetime


class SessionExpAuth(SessionAuth):
    """
        SessionExpAuth - Session Authentication Expiration
    """
    user_id_by_session_id = {}

    def __init__(self):
        """ initialize """
        super().__init__()
        session_duration = getenv('SESSION_DURATION')
        if not session_duration:
            self.session_duration = 0
        try:
            self.session_duration = int(session_duration)
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """
            create session
            Arguments:
                user_id: the user id
            Return:
                Session ID or None
        """
        if not user_id:
            return None
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dict = {'user_id': user_id, 'created_at': datetime.now()}
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
            user_id_for_session_id
            Arguments:
                session_id: session id
            Return:
                user id
        """
        if not session_id:
            return None
        user_dict = self.user_id_by_session_id.get(session_id)
        if not user_dict:
            return None
        if self.session_duration <= 0:
            return user_dict.get('user_id')
        if not user_dict.get('created_at'):
            return None
        duration = timedelta(seconds=self.session_duration)
        exp = user_dict.get('created_at') + duration
        if exp < datetime.now():
            return None
        return user_dict.get('user_id')
