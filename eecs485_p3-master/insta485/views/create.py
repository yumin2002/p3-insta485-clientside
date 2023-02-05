"""
Insta485 login view.

URLs include:
/accounts/login/
"""
import hashlib
import os
import shutil
import tempfile

import flask
from flask import abort
from flask import request
from flask import session

import insta485


def check_existing(username):
    """Docstring."""
    d_b = insta485.model.get_db()
    i_t = d_b.cursor()
    user = i_t.execute('SELECT * FROM users WHERE username=?',
                       (username,)).fetchone()
    i_t.connection.commit()
    if user is None:
        return False
    return True


def sha256sum(filename):
    """Return sha256 hash of file content, similar to UNIX sha256sum."""
    content = open(filename, 'rb').read()
    sha256_obj = hashlib.sha256(content)
    return sha256_obj.hexdigest()


@insta485.app.route('/accounts/create/', methods=['GET', 'POST'])
def create():
    """Display /accounts/login/ route."""
    if request.method == 'GET':
        if 'logname' in session:
            return flask.redirect("/accounts/edit/", code=302)
        context = {}
        return flask.render_template("create.html", **context)

    file = request.files['file']
    # Save POST request's file object to a temp file
    dummy, temp_filename = tempfile.mkstemp()
    file.save(temp_filename)

    # Compute filename
    hash_txt = sha256sum(temp_filename)
    # what the f
    dummy, suffix = os.path.splitext(file.filename)
    # stupid pylint
    hash_filename_basename = hash_txt + suffix
    # lemme pass
    hash_filename = os.path.join(
        insta485.app.config["UPLOAD_FOLDER"],
        hash_filename_basename
    )

    # Move temp file to permanent location
    shutil.move(temp_filename, hash_filename)
    insta485.app.logger.debug("Saved %s", hash_filename_basename)

    fullname = request.form['fullname']
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    if check_existing(username) is True:
        print("Username already exists")
        abort(409)
    if not password:
        print("Password empty")
        abort(400)

    d_b = insta485.model.get_db()
    i_t = d_b.cursor()
    i_t.execute("INSERT INTO users (username, fullname, email,"
                "filename, password) VALUES (?, ?, ?, ?, ?)",
                (username, fullname, email, hash_filename_basename,
                 insta485.utility.hash_password(password),))

    session['logname'] = username
    session['fullname'] = fullname
    session['email'] = email
    session['filename'] = hash_filename_basename
    session['password'] = password
    return flask.redirect('/')
