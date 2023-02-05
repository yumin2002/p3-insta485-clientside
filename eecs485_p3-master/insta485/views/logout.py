"""
Insta485 login view.

URLs include:
/accounts/login/
"""
import flask
from flask import session

import insta485


@insta485.app.route('/accounts/logout/', methods=['GET', 'POST'])
def logout():
    """Display /accounts/login/ route."""
    session.clear()
    return flask.redirect('/accounts/login/', code=302)
