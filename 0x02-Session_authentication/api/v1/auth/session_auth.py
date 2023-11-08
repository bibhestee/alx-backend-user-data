#!/usr/bin/env python3
"""
    Session Authentication Module
"""
from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """
        SessionAuth - Session Authentication
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
            create session
            Arguments:
                user_id: the user id
            Return:
                Session ID or None
        """
        if not user_id or type(user_id) != str:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
            user_id_for_session_id - get user id based on session id
            Arguments:
                session_id: session id
            Return:
                User id or None
        """
        if not session_id or type(session_id) != str:
            return None
        return self.user_id_by_session_id.get(session_id)
