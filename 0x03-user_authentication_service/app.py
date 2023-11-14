#!/usr/bin/env python3
"""
Flask app
"""
from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', strict_slashes=False)
def home():
    """ Home route """
    return jsonify({'message': 'Bienvenue'})


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
        return jsonify({'message': 'email already registered'}), 400
    # return success message if user is created
    payload = {'email': user.email, 'message': 'user created'}
    return jsonify(payload)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
