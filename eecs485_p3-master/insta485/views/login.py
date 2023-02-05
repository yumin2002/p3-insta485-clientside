"""
Insta485 login view.

URLs include:
/accounts/login/
"""
import flask
from flask import request, session

import insta485


@insta485.app.route('/accounts/login/', methods=['GET', 'POST'])
def login():
    """Display /accounts/login/ route."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        d_b = insta485.model.get_db()
        i_t = d_b.cursor()
        user = i_t.execute('SELECT * FROM users WHERE username=?',
                           (username,)).fetchone()

        if user is None:
            print("Username doen't exist")
            return flask.redirect('/accounts/login')
        if not insta485.utility.valid(username, password):
            print("Password incorrect")
            return flask.redirect('/accounts/login')

        session['logname'] = username
        session['fullname'] = user['fullname']
        session['email'] = user['email']
        session['filename'] = user['filename']
        session['password'] = password
        return flask.redirect('/')
    if 'logname' in session:
        return flask.redirect('/', code=302)
    context = {}
    return flask.render_template("login.html", **context)
