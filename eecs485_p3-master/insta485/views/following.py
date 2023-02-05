"""Docstring."""

import flask
import insta485

# This is following.py created by Jiajun Peng
# avoid duplicate


def create_context(user):
    """Docstring."""
    hello = insta485.model.get_db()
    cursor = hello.cursor()
    context = {}
    context['logname'] = flask.session['logname']
    following = []

    # get all the following of user(at this page)
    follow = []
    for line in cursor.execute("SELECT * FROM following WHERE username1=?",
                               (user,)):
        follow.append(line['username2'])

    for people in follow:
        info = {}
        info['username'] = people

        # user image url
        for url in cursor.execute("SELECT * FROM users WHERE username=?",
                                  (people,)):
            info['user_img_url'] = '/uploads/' + url['filename']

        # logname_follows_username
        info['logname_follows_username'] = False
        for data in cursor.execute(
                "SELECT * FROM following WHERE username2=?", (people,)):
            if data['username1'] == flask.session['logname']:
                info['logname_follows_username'] = True

        following.append(info)

    context['following'] = following
    return context


@insta485.app.route('/u/<user>/following/', methods=['GET', 'POST'])
def show_following(user):
    """Docstring."""
    if flask.request.method == 'GET':
        if 'logname' not in flask.session:
            return flask.redirect('/accounts/login/', code=302)
    else:
        if 'logname' not in flask.session:
            flask.abort(403)
        temp = insta485.model.get_db()
        cursor = temp.cursor()
        if 'follow' in flask.request.form:
            cursor.execute(
                "INSERT INTO following (username1, username2) VALUES (?,?)",
                (flask.session['logname'], flask.request.form['username']))
        if 'unfollow' in flask.request.form:
            cursor.execute(
                "DELETE FROM following WHERE username1=? AND username2=?",
                (flask.session['logname'], flask.request.form['username']))
        temp.commit()

    context = create_context(user)
    return flask.render_template('following.html', **context)
