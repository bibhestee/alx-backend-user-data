#!/usr/bin/env python3
"""
    Session DB Authentication Module
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
        SessionDBAuth - Session DB Authentication
    """

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
        if session_id:
            session = UserSession()
            session.user_id = user_id
            session.session_id = session_id
            session.save()
            return session.session_id
        return null

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
        user_session = UserSession.search({'session_id': session_id})
        if user_session[0]:
            return user_session[0].user_id
        return None

    def destroy_session(self, request=None):
        """
            destroy session
            Arguments:
                request: flask request method
            Return:
                None
        """
        session_id = self.session_cookie(request)
        u_session = UserSession()
        super().destroy_session()
        u_session.remove(session_id)
