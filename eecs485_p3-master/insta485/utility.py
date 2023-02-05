"""Insta485 utility API."""

import uuid
import hashlib
import insta485


def hash_password(p_w):
    """Docstring."""
    algorithm = 'sha512'
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + p_w
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    return password_db_string


def hash_old_password(salt, p_w):
    """Docstring."""
    algorithm = 'sha512'
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + p_w
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    return password_hash


def valid(username, password):
    """Docstring."""
    d_b = insta485.model.get_db()
    i_t = d_b.cursor()
    i_t.execute('SELECT password FROM users WHERE username=?', (username,))
    db_password = i_t.fetchone()["password"]

    split_db_password = db_password.split('$')
    algorithm = split_db_password[0]
    salt = split_db_password[1]
    hash_db_password = split_db_password[2]

    # algorithm = 'sha512'
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()

    if hash_db_password != password_hash:
        return False

    return True
