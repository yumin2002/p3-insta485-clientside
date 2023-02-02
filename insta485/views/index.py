"""
Insta485 index (main) view.

URLs include:
/
"""
import os
import flask
import arrow
import insta485
import insta485.views.accounts


@insta485.app.route('/')
def show_index():
    """Display / route."""
    # If not logged in, redirect to /accounts/login/
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_account_login'))

    # Connect to database
    connection = insta485.model.get_db()
    # get logname
    logname = flask.session['username']
    # select all posts posted by users that the logname is following
    cur = connection.execute(
        "SELECT postid, filename, owner, created "
        "FROM posts "
        "WHERE owner IN "
        "(SELECT username2 FROM following WHERE (username1 == ?)) "
        "OR (owner == ? ) "
        "ORDER BY postid DESC",
        (logname, logname, )
    )
    posts = cur.fetchall()
    # humanize time, add like and comments attribute to the posts
    for post in posts:
        # fix time stamp
        time = arrow.get(post['created'])
        post['created'] = time.humanize()
        # get profile picture
        cur = connection.execute(
            "SELECT filename FROM users "
            "WHERE username == ?",
            (post['owner'],)
        )
        pic = cur.fetchall()[0]['filename']
        post['profile_pic'] = pic
        # add number of likes
        cur = connection.execute(
            "SELECT postid FROM likes "
            "WHERE postid == ?",
            (post['postid'],)
        )
        num_likes = len(cur.fetchall())
        post['likes'] = num_likes
        # add if the logname has liked the post
        cur = connection.execute(
            "SELECT owner FROM likes "
            "WHERE postid == ? AND owner == ?",
            (post['postid'], logname, )
        )
        logname_like = (len(cur.fetchall()))
        if logname_like != 0:
            post['liked'] = True
        else:
            post['liked'] = False
        # add a list of comments for the post
        cur = connection.execute(
            "SELECT owner, text FROM comments "
            "WHERE postid == ?"
            "ORDER BY commentid ASC",
            (post['postid'], )
        )
        post['comments'] = cur.fetchall()
    # Add database info to context
    context = {"posts": posts, "logname": logname}
    # return posts
    return flask.render_template("index.html", **context)


@insta485.app.route('/uploads/<path:filename>')
def send_file(filename):
    """Send file."""
    if 'username' not in flask.session:
        flask.abort(403)
    if not os.path.exists(f'var/uploads/{filename}'):
        flask.abort(404)
    return flask.send_from_directory(
        insta485.app.config['UPLOAD_FOLDER'],
        filename)


@insta485.app.route('/posts/<postid_url_slug>/')
def show_post(postid_url_slug):
    """Display / route."""
    # Connect to database
    connection = insta485.model.get_db()

    # get logname
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for("show_account_login"))
    logname = flask.session['username']

    # get post owner, post image, and timestamp from post
    cur = connection.execute(
        "SELECT owner, postid, filename, created FROM posts "
        "WHERE postid == ?",
        (postid_url_slug, )
    )
    post = cur.fetchall()

    # error checking: if postid does not exist
    if len(post) == 0:
        flask.abort(404)

    # return post
    timestamp = arrow.get(post[0]['created'])
    post[0]['created'] = timestamp.humanize()

    # get if post owner is the loguser
    logname_own_post = False
    cur = connection.execute(
        "SELECT owner FROM posts "
        "WHERE postid == ? "
        "AND owner == ?",
        (postid_url_slug, logname)
    )
    if len(cur.fetchall()) == 0:
        logname_own_post = False
    else:
        logname_own_post = True

    # get profile picture from users
    cur = connection.execute(
        "SELECT filename FROM users "
        "WHERE username == ?",
        (post[0]['owner'], )
    )
    pic_filename = cur.fetchall()[0]['filename']

    # get number of likes from likes
    cur = connection.execute(
        "SELECT likeid FROM likes "
        "WHERE postid == ?",
        (postid_url_slug, )
    )
    likes = len(cur.fetchall())

    # get if the logname has liked the post from likes
    liked = False
    cur = connection.execute(
        "SELECT likeid FROM likes "
        "WHERE owner == ? "
        "AND postid == ?",
        (logname, postid_url_slug, )
    )
    if len(cur.fetchall()) == 0:
        liked = False
    else:
        liked = True

    # get owner and text for all the comments
    cur = connection.execute(
        "SELECT owner, text, commentid FROM comments "
        "WHERE postid == ? "
        "ORDER BY commentid ASC",
        (postid_url_slug, )
    )
    comments = cur.fetchall()

    # for each comment, check if the comment belong to the logname
    for comment in comments:
        if comment['owner'] == logname:
            comment['belong_to_logname'] = True
        else:
            comment['belong_to_logname'] = False

    # Add database info to context
    context = {
        "post": post,
        "logname": logname,
        "logname_own_post": logname_own_post,
        "pic_filename": pic_filename,
        "likes": likes,
        "liked": liked,
        "comments": comments
    }

    # return posts
    return flask.render_template("post.html", **context)


@insta485.app.route('/explore/')
def show_explore():
    """Display / route."""
    # If not logged in, redirect to /accounts/login/
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_account_login'))

    # Connect to database
    connection = insta485.model.get_db()

    # get logname
    logname = flask.session['username']

    # get all the users that the logname is not following
    cur = connection.execute(
        "SELECT username, filename FROM users "
        "WHERE username NOT IN "
        "(SELECT username2 FROM following WHERE username1 == ?) "
        "AND username != ?",
        (logname, logname, )
    )

    not_following = cur.fetchall()
    context = {"not_following": not_following, "logname": logname}
    return flask.render_template("explore.html", **context)


@insta485.app.route('/likes/', methods=['POST'])
def update_likes():
    """Update number of likes after like or unlike."""
    # If not logged in, redirect to /accounts/login/
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_account_login'))

    # Connect to database
    connection = insta485.model.get_db()

    # get logname
    logname = flask.session['username']

    # get postid
    postid = flask.request.form.get("postid")

    # check if the user has liked the post before
    liked = False
    cur = connection.execute(
        "SELECT owner FROM likes WHERE owner == ? AND postid == ?",
        (logname, postid, )
    )
    if len(cur.fetchall()) == 0:
        liked = False
    else:
        liked = True

    # like already liked or unlike already unliked post
    if (flask.request.form.get("operation") == "like" and liked) \
            or (flask.request.form.get("operation") == "unlike" and not liked):
        flask.abort(409)

    # like operation
    if (flask.request.form.get("operation") == "like") and not liked:
        cur = connection.execute(
            "INSERT INTO likes (owner, postid) VALUES (?, ?) ",
            (logname, postid, )
        )
        # return statement
        if flask.request.args.get('target') is None:
            return flask.redirect("/")
        return flask.redirect(flask.request.args.get('target'))

    # unlike operation
    if (flask.request.form.get("operation") == "unlike") and liked:
        connection.execute(
            "DELETE FROM likes WHERE owner == ? AND postid == ?",
            (logname, postid, )
        )
        cur = connection.execute(
            "SELECT likeid, owner, postid FROM likes"
        )
        # return statement
        if flask.request.args.get('target') is None:
            return flask.redirect("/")
        return flask.redirect(flask.request.args.get('target'))

    # other illegal operation
    flask.abort(500)
    return None


@insta485.app.route('/comments/', methods=['POST'])
def update_comments():
    """Post a new comment or delete for the post."""
    # If not logged in, redirect to /accounts/login/
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_account_login'))

    # Connect to database
    connection = insta485.model.get_db()

    # get logname
    # logname = "awdeorio"
    logname = flask.session['username']
    operation = flask.request.form.get('operation')

    # create comment
    if operation == "create":
        # get variables in form
        postid = flask.request.form.get('postid')
        text = flask.request.form.get('text')

        # ERROR CHECKING: create empty comment
        if (text == "" or text is None):
            flask.abort(400)

        cur = connection.execute(
            "INSERT INTO comments (owner, postid, text) VALUES (?, ?, ?)",
            (logname, postid, text)
        )

        if flask.request.args.get('target') is None:
            return flask.redirect("/")
        return flask.redirect(flask.request.args.get('target'))

    # delete comment
    # get variable in form
    commentid = flask.request.form.get('commentid')

    # ERROR CHECKING: check if logname owns the comment
    cur = connection.execute(
        "SELECT owner FROM comments WHERE owner == ? AND commentid == ?",
        (logname, commentid, )
    )

    # not owner of the comment
    if len(cur.fetchall()) == 0:
        flask.abort(403)

    # remove comment from database
    cur = connection.execute(
        "DELETE FROM comments WHERE commentid == ?",
        (commentid, )
    )
    if flask.request.args.get('target') is None:
        return flask.redirect("/")
    return flask.redirect(flask.request.args.get('target'))


@insta485.app.route('/posts/', methods=['POST'])
def update_posts():
    """Create a new post or delete for the post."""
    # If not logged in, redirect to /accounts/login/
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_account_login'))

    # Connect to database
    connection = insta485.model.get_db()

    # get logname
    # logname = "awdeorio"
    logname = flask.session['username']
    operation = flask.request.form.get('operation')
    postid = flask.request.form.get('postid')

    if operation == "delete":
        # postid = flask.request.form.get('postid')

        # ERROR CHECKING: logname does not own the post
        cur = connection.execute(
            "SELECT owner FROM posts WHERE owner == ? AND postid == ?",
            (logname, postid, )
        )
        if len(cur.fetchall()) == 0:
            flask.abort(403)

        # delete from upload
        cur = connection.execute(
            "SELECT filename FROM posts WHERE postid == ?",
            (postid, )
        )

        filename = cur.fetchall()[0]['filename']
        path = 'var/uploads/'
        path = os.path.join(path, filename)
        os.remove(path)

        # delete the post info from the database
        cur = connection.execute(
            "DELETE FROM posts WHERE postid == ?",
            (postid, )
        )
        cur = connection.execute(
            "DELETE FROM likes WHERE postid == ?",
            (postid, )
        )
        cur = connection.execute(
            "DELETE FROM comments WHERE postid == ?",
            (postid, )
        )

        if flask.request.args.get('target') is None:
            return flask.redirect(f"/users/{logname}/")
        return flask.redirect(flask.request.args.get('target'))
    # else:
    if "file" not in flask.request.files:
        flask.abort(400)

    # hash filename
    uuid_basename = insta485.views.accounts.hashing()

    connection.execute(
        "INSERT into posts (filename, owner) "
        "VALUES (?, ?)",
        (uuid_basename, logname)
    )
    if flask.request.args.get('target') is None:
        return flask.redirect(f"/users/{logname}/")
    return flask.redirect(flask.request.args.get('target'))


@insta485.app.route("/users/<user_url_slug>/")
def show_users(user_url_slug):
    """Show user page."""
    if 'username' in flask.session:
        logname = flask.session['username']
    # add back when session is created
    else:
        return flask.redirect(flask.url_for("show_account_login"))

    # Connect to database
    connection = insta485.model.get_db()
    # username_to_display = user_url_slug
    # check if user exist
    cur = connection.execute(
        "SELECT username FROM users WHERE username == ?",
        (user_url_slug, )
    )
    user_exist = cur.fetchall()
    if len(user_exist) == 0:
        flask.abort(404)

    cur = connection.execute(
        "SELECT username2 FROM following WHERE username1 == ?",
        (logname, )
    )
    relationship = cur.fetchall()

    cur = connection.execute(
        "SELECT count(owner) FROM posts WHERE owner == ?",
        (user_url_slug, )
    )
    total_posts = cur.fetchall()[0]['count(owner)']

    cur = connection.execute(
        "SELECT fullname FROM users WHERE username == ?",
        (user_url_slug, )
    )
    name = cur.fetchall()[0]['fullname']

    connection.execute(
        "SELECT filename FROM posts WHERE owner == ?",
        (user_url_slug,)
    )
    # followers
    cur = connection.execute(
        "SELECT count(username1) FROM following WHERE username2 == ?",
        (user_url_slug,)
    )
    followers = cur.fetchall()[0]['count(username1)']

    # following
    cur = connection.execute(
        "SELECT count(username2) FROM following WHERE username1 == ?",
        (user_url_slug,)
    )
    following = cur.fetchall()[0]['count(username2)']

    # posts
    cur = connection.execute(
        "SELECT postid, filename, owner "
        "FROM posts "
        "WHERE owner == ?",
        (user_url_slug,)
    )
    posts = cur.fetchall()

    cur = connection.execute(
        "SELECT username2 "
        "FROM following "
        "WHERE username1 == ?",
        (logname,)
    )
    log_following = cur.fetchall()
    # for post in posts:
    log_follows_user = 0
    for user in log_following:
        if user_url_slug == user["username2"]:
            log_follows_user = 1
    relationship = log_follows_user
    log_follows_user = 0
    context = {
        "logname": logname,
        "username": user_url_slug,
        "total_posts": total_posts,
        "followers": followers,
        "following": following,
        "posts": posts,
        "logname_follows_username": relationship,
        "fullname": name
    }
    return flask.render_template("users.html", **context)


@insta485.app.route("/users/<user_url_slug>/following/")
def show_following(user_url_slug):
    """Show following page."""
    target = f"/users/{user_url_slug}/following/"
    if 'username' in flask.session:
        logname = flask.session['username']
    # add back when session is created
    else:
        return flask.redirect(flask.url_for("show_account_login"))
    username = user_url_slug
    # Connect to database
    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT username FROM users WHERE username == ?",
        (username, )
    )
    user_exist = cur.fetchall()
    if len(user_exist) == 0:
        flask.abort(404)

    # get the people the user follows
    cur = connection.execute(
        "SELECT username2 "
        "FROM following "
        "WHERE username1 == ?",
        (user_url_slug,)
    )
    user_following = cur.fetchall()

    for user in user_following:
        cur = connection.execute(
            "SELECT filename "
            "FROM users "
            "WHERE username == ?",
            (user['username2'],)
        )

        cur1 = cur.fetchall()
        user["filename"] = cur1[0]["filename"]

    for user in user_following:
        cur = connection.execute(
            "SELECT username1, username2 "
            "FROM following "
            "WHERE username1 == ? AND username2 == ?",
            (logname, user['username2'])
        )
        log_following = cur.fetchall()
        if logname == user['username2']:
            user["following"] = -1
        elif len(log_following) == 0:
            user["following"] = 0
        elif len(log_following) > 0:
            user["following"] = 1

    context = {
        "target": target,
        "username": username,
        "logname": logname,
        "dict": user_following,
    }
    return flask.render_template("following.html", **context)


@insta485.app.route("/users/<user_url_slug>/followers/")
def show_follower(user_url_slug):
    """Show follower page."""
    target = f"/users/{user_url_slug}/followers/"
    if 'username' in flask.session:
        logname = flask.session['username']
    # add back when session is created
    else:
        return flask.redirect(flask.url_for("show_account_login"))
    username = user_url_slug
    # Connect to database
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT username FROM users WHERE username == ?",
        (username, )
    )
    user_exist = cur.fetchall()
    if len(user_exist) == 0:
        flask.abort(404)

    cur = connection.execute(
        "SELECT username1 FROM following WHERE username2 == ?",
        (username,)
    )
    user_follower = cur.fetchall()

    for user in user_follower:
        cur = connection.execute(
            "SELECT filename FROM users WHERE username == ?",
            (user['username1'],)
        )
        cur1 = cur.fetchall()
        user["filename"] = cur1[0]["filename"]

    for user in user_follower:
        cur = connection.execute(
            "SELECT username1, username2 "
            "FROM following "
            "WHERE username1 == ? AND username2 == ?",
            (logname, user['username1'])
        )
        log_following = cur.fetchall()
        if logname == user['username1']:
            user["following"] = -1
        elif len(log_following) == 0:
            user["following"] = 0
        elif len(log_following) > 0:
            user["following"] = 1

    context = {
        "target": target,
        'username': username,
        "logname": logname,
        "dict": user_follower
    }
    return flask.render_template("followers.html", **context)


@insta485.app.route('/following/', methods=['POST'])
def update_following():
    """Follows or unfollows a user and immediately redirect to URL."""
    connection = insta485.model.get_db()

    if 'username' in flask.session:
        logname = flask.session['username']
    # add back when session is created
    else:
        return flask.redirect(flask.url_for("show_account_login"))
    username = flask.request.form.get("username")
    operation = flask.request.form.get("operation")
    if operation == "follow":
        # check if logname already follows username
        cur = connection.execute(
            "SELECT username2 FROM following "
            "WHERE username1 == ? ",
            (logname, ))
        logname_follows = cur.fetchall()
        following = []
        for item in logname_follows:
            following.append(item['username2'])
        if username in following:
            flask.abort(409)
        # add this follow entry to database
        cur1 = connection.execute(
            "INSERT into following "
            "(username1, username2) "
            "VALUES (?, ?)",
            (logname, username)
        )
        if flask.request.args.get('target') is None:
            return flask.redirect("/")
        return flask.redirect(flask.request.args.get('target'))
    if operation == "unfollow":
        # check if logname already follows username
        cur1 = connection.execute(
            "SELECT username2 FROM following "
            "WHERE username1 == ? ",
            (logname, ))
        logname_follows = cur1.fetchall()
        following = []

        for item in logname_follows:
            following.append(item['username2'])
        if username not in following:
            flask.abort(409)
        # add this follow entry to database
        cur = connection.execute(
            "DELETE FROM following "
            "WHERE username1 == ? AND username2 ==?",
            (logname, username))
        if flask.request.args.get('target') is None:
            return flask.redirect("/")
        return flask.redirect(flask.request.args.get('target'))
    return "operation not follow for unfollow"
