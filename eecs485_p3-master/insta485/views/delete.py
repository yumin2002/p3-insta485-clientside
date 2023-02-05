"""
Insta485 login view.

URLs include:
/accounts/login/
"""
import os

import flask
from flask import request, session

import insta485


@insta485.app.route('/accounts/delete/', methods=['GET', 'POST'])
def delete():
    """Display /accounts/login/ route."""
    if request.method == 'GET':
        if "logname" not in session:
            return flask.redirect("/accounts/login/")
        context = {}
        context['logname'] = session['logname']
        return flask.render_template("delete.html", **context)

    username = session['logname']

    d_b = insta485.model.get_db()
    i_t = d_b.cursor()

    path = os.path.join(
        insta485.app.config["UPLOAD_FOLDER"],
        i_t.execute("SELECT filename FROM users WHERE username=?",
                    (username,)).fetchone()['filename']
    )
    os.remove(path)

    for post in i_t.execute("SELECT * FROM posts WHERE owner=?", (username,)):
        path = os.path.join(
            insta485.app.config["UPLOAD_FOLDER"],
            post['filename']
        )
        # print(path)
        os.remove(path)

    i_t.execute("DELETE FROM users WHERE username=?", (username,))
    i_t.connection.commit()

    session.clear()

    return flask.redirect("/accounts/create/")
