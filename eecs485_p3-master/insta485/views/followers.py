"""Docstring."""
import flask
import insta485

# This is followers.py created by Jiajun Peng


def create_context(user):
    """Docstring."""
    datab = insta485.model.get_db()
    cursor = datab.cursor()
    context = {}
    context['logname'] = flask.session['logname']
    followers = []

    # get all the followers of user
    follower = []
    for row in cursor.execute("SELECT * FROM following WHERE username2=?",
                              (user,)):
        follower.append(row['username1'])

    for people in follower:
        temp = {}
        temp['username'] = people

        # user image url
        for image in cursor.execute("SELECT * FROM users WHERE username=?",
                                    (people,)):
            temp['user_img_url'] = '/uploads/' + image['filename']

        # logname_follows_username
        temp['logname_follows_username'] = False
        for info in cursor.execute(
                "SELECT * FROM following WHERE username2=?", (people,)):
            if info['username1'] == flask.session['logname']:
                temp['logname_follows_username'] = True

        followers.append(temp)

    context['followers'] = followers
    return context


@insta485.app.route('/u/<user>/followers/', methods=['GET', 'POST'])
def show_followers(user):
    """Docstring."""
    if flask.request.method == 'POST':
        if 'logname' not in flask.session:
            flask.abort(403)
        datab = insta485.model.get_db()
        cursor = datab.cursor()
        if 'follow' not in flask.request.form:
            pass
        else:
            cursor.execute(
                "INSERT INTO following (username1, username2) VALUES (?,?)",
                (flask.session['logname'], flask.request.form['username']))
        if 'unfollow' not in flask.request.form:
            pass
        else:
            cursor.execute(
                "DELETE FROM following WHERE username1=? AND username2=?",
                (flask.session['logname'], flask.request.form['username']))
        datab.commit()

    else:
        if 'logname' not in flask.session:
            return flask.redirect('/accounts/login/', code=302)

    context = create_context(user)

    return flask.render_template('followers.html', **context)
