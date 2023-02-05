"""Hey."""
import flask
from flask import abort, session, request
import insta485


@insta485.app.route('/accounts/password/', methods=['GET', 'POST'])
def password():
    """Display /accounts/login/ route."""
    if request.method == 'GET':
        context = {}
        context['logname'] = session['username']
        return flask.render_template("password.html", **context)

    old_password = request.form['password']
    new_password1 = request.form['new_password1']
    new_password2 = request.form['new_password2']

    d_b = insta485.model.get_db()
    i_t = d_b.cursor()
    pass_word = i_t.execute("SELECT password FROM users WHERE username=?",
                            (session['username'],)).fetchone()['password']

    split_db_password = pass_word.split('$')
    salt = split_db_password[1]
    hash_old = insta485.utility.hash_old_password(salt, old_password)
    hash_db_password = split_db_password[2]

    if not new_password1:
        print("Password empty")
        abort(400)
    if new_password1 != new_password2:
        print("Second password doesn't match with the first")
        abort(401)
    if hash_db_password != hash_old:
        print("Old password incorrect")
        abort(403)

    session['password'] = request.form['new_password1']
    hash_new = insta485.utility.hash_password(new_password2)
    i_t.execute("UPDATE users SET password=?"
                "WHERE username=?",
                (hash_new, session['username'],))
    i_t.connection.commit()

    return flask.redirect('/accounts/edit/')
