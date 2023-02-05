"""Docstring."""
import flask
import insta485


def create_context():
    """Docstring."""
    datab = insta485.model.get_db()
    cursor = datab.cursor()
    context = {}
    context['logname'] = flask.session['logname']
    not_following = []

    # get all the following of logged-in user
    follow = []
    for data in cursor.execute("SELECT * FROM following WHERE username1=?",
                               (flask.session['logname'],)):
        follow.append(data['username2'])
    follow.append(flask.session['logname'])

    # get all the not following of logged_in user
    not_follow = []
    for user in cursor.execute("SELECT * FROM users"):
        if user['username'] not in follow:
            not_follow.append(user['username'])

    for user in not_follow:
        info = {}
        info['username'] = user

        # user image url
        for data in cursor.execute("SELECT * FROM users WHERE username=?",
                                   (user,)):
            info['user_img_url'] = '/uploads/' + data['filename']
        not_following.append(info)

    context['not_following'] = not_following
    return context


@insta485.app.route('/explore/', methods=['GET', 'POST'])
def show_explore():
    """Docstring."""
    if flask.request.method == 'POST':
        if 'logname' not in flask.session:
            flask.abort(403)
        datatemp = insta485.model.get_db()
        cursor = datatemp.cursor()
        if 'follow' in flask.request.form:
            cursor.execute(
                "INSERT INTO following (username1, username2) VALUES (?,?)",
                (flask.session['logname'], flask.request.form['username']))
        datatemp.commit()
    else:
        if 'logname' not in flask.session:
            return flask.redirect('/accounts/login/', code=302)

    context = create_context()
    return flask.render_template('explore.html', **context)
