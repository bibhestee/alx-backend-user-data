#!/usr/bin/env python3
""" Module of Session Authentication views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ POST /api/v1/auth_session/login
    Return:
        - None
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    user = User.search({'email': email})
    if not user or user == []:
        return jsonify({"error": "no user found for this email"}), 404
    valid_pwd = user[0].is_valid_password(password)
    if not valid_pwd:
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(email)
    session_tip = getenv('SESSION_NAME')
    # Jsonify returns a Response Object
    response = jsonify(user[0].to_json())
    response.set_cookie(session_tip, session_id)
    return response
