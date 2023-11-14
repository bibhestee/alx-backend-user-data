#!/usr/bin/env python3
"""
Main file
"""
import requests

base_url = 'http://127.0.0.1:5000'


def register_user(email: str, password: str) -> None:
    """ register user """
    # expected outputs
    status_code = 200
    exp_payload = {'email': email, 'message': 'user created'}
    # start test
    url = base_url + '/users'
    data = {'email': email, 'password': password}
    res = requests.post(url, data)
    assert res.status_code == status_code
    assert res.json() == exp_payload


def log_in_wrong_password(email: str, password: str) -> None:
    """ login with wrong password """
    # expected outputs
    status_code = 401
    # start test
    url = base_url + '/sessions'
    data = {'email': email, 'password': password}
    res = requests.post(url, data)
    assert res.status_code == status_code


def log_in(email: str, password: str) -> str:
    """ login """
    # expected outputs
    status_code = 200
    exp_payload = {'email': email, 'message': 'logged in'}
    # start test
    url = base_url + '/sessions'
    data = {'email': email, 'password': password}
    res = requests.post(url, data)
    print(res)
    assert res.status_code == status_code
    assert res.json() == exp_payload
    return res.cookies.session_id


def profile_unlogged() -> None:
    """ profile unlogged """
    # expected outputs
    status_code = 403
    # start test
    url = base_url + '/profile'
    res = requests.get(url)
    assert res.status_code == status_code


def profile_logged(session_id: str) -> None:
    """ profile logged """
    # expected outputs
    status_code = 200
    exp_payload = {'email': email}
    # start test
    url = base_url + '/profile'
    data = {'session_id': session_id}
    res = requests.get(url, data)
    assert res.status_code == status_code
    assert res.json() == exp_payload


def log_out(session_id: str) -> None:
    """ logout """
    # expected outputs
    status_code = 200
    # start test
    url = base_url + '/sessions'
    data = {'session_id': session_id}
    res = requests.delete(url, data)
    assert res.status_code == status_code


def reset_password_token(email: str) -> str:
    """ reset password token """
    # expected outputs
    status_code = 200
    # start test
    url = base_url + '/reset_password'
    data = {'email': email}
    res = requests.post(url, data)
    response = res.json()
    assert res.status_code == status_code
    assert hasattr(response, 'email')
    assert hasattr(response, 'reset_token')
    return response.get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ update password """
    # expected outputs
    status_code = 200
    exp_payload = {'email': email, 'message': 'Password updated'}
    # start test
    url = base_url + '/reset_password'
    data = {'email': email, 'reset_token': reset_token, 'new_password':
            new_password}
    res = requests.put(url, data)
    assert res.status_code == status_code
    assert res.json() == exp_payload


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
