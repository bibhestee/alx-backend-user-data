#!/usr/bin/env python3
"""
Flask app
"""
from flask import Flask, jsonify, request, make_response, abort
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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
