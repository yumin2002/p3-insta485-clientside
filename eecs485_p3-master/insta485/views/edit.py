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
from flask import request
from flask import session
import insta485


def sha256sum(filename):
    """Return sha256 hash of file content, similar to UNIX sha256sum."""
    content = open(filename, 'rb').read()
    sha256_obj = hashlib.sha256(content)
    return sha256_obj.hexdigest()


@insta485.app.route('/accounts/edit/', methods=['GET', 'POST'])
def edit():
    """Display /accounts/login/ route."""
    if request.method == 'GET':
        context = {}
        context['logname'] = session['logname']
        context['filename'] = session['filename']
        context['fullname'] = session['fullname']
        context['email'] = session['email']
        return flask.render_template("edit.html", **context)

    # print(request.files)
    file = request.files.get('file')
    if file is not None:
        path = os.path.join(
            insta485.app.config["UPLOAD_FOLDER"], session['filename']
        )
        os.remove(path)

        # Save POST request's file object to a temp file
        dummy, temp_fil = tempfile.mkstemp()
        file.save(temp_fil)

        # Compute filename
        hash_txt = sha256sum(temp_fil)
        # not same
        dummy, suffix = os.path.splitext(file.filename)
        # not same at all
        hash_filename_basename = hash_txt + suffix
        hash_filename = os.path.join(
            insta485.app.config["UPLOAD_FOLDER"],
            # why so stupid
            hash_filename_basename
        )

        # Move temp file to permanent location
        shutil.move(temp_fil, hash_filename)
        insta485.app.logger.debug("Saved %s", hash_filename_basename)

        session['filename'] = hash_filename_basename

    username = session['logname']
    fullname = request.form['fullname']
    email = request.form['email']

    d_b = insta485.model.get_db()
    i_t = d_b.cursor()
    i_t.execute("UPDATE users SET fullname=?, email=? "
                "WHERE username=?", (fullname, email, username,))
    if file is not None:
        i_t.execute("UPDATE users SET filename=?"
                    "WHERE username=?",
                    (hash_filename_basename, username,))
    i_t.connection.commit()

    session['fullname'] = fullname
    session['email'] = email

    context = {}
    context['logname'] = session['logname']
    context['filename'] = session['filename']
    context['fullname'] = session['fullname']
    context['email'] = session['email']
    return flask.render_template("edit.html", **context)
