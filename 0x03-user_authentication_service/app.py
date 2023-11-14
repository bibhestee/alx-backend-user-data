#!/usr/bin/env python3
"""
Flask app
"""
from flask import Flask
from flask import redirect, jsonify, request, make_response, abort, url_for
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', strict_slashes=False)
def home():
    """ Home route """
    payload = {'message': 'Bienvenue'}
    return jsonify(payload)


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """ register a new user """
    # get the data fields
    req = request.form.to_dict()
    try:
        email = req.get('email')
        password = req.get('password')
        user = AUTH.register_user(email, password)
    except ValueError:
        payload = {'message': 'email already registered'}
        return jsonify(payload), 400
    # return success message if user is created
    payload = {'email': user.email, 'message': 'user created'}
    return jsonify(payload)


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """ login """
    # get the form data from request
    req = request.form.to_dict()
    email = req.get('email')
    password = req.get('password')
    valid = AUTH.valid_login(email, password)
    if valid:
        session_id = AUTH.create_session(email)
        payload = {'email': email, 'message': 'logged in'}
        res = make_response(jsonify(payload))
        res.set_cookie('session_id', session_id)
        return res
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """ logout """
    # get the cookie from request
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for('home'))
    else:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """ profile """
    # get the cookie from request
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        payload = {'email': user.email}
        return jsonify(payload)
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """ get reset password token """
    # get the form data from request
    req = request.form.to_json()
    email = req.get('email')
    try:
        user = AUTH._db.find_user_by(email=email)
        token = AUTH.get_reset_password_token(email)
        payload = {'email': email, 'reset_token': token}
        return jsonify(payload)
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
