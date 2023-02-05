"""
Insta485 user (main) view.

URLs include:
/
"""
import os
import shutil
import tempfile
import hashlib
import flask
from flask import request, session, send_from_directory
import insta485
import insta485.model
import insta485.config


def sha256sum(filename):
    """Return sha256 hash of file content, similar to UNIX sha256sum."""
    content = open(filename, 'rb').read()
    sha256_obj = hashlib.sha256(content)
    return sha256_obj.hexdigest()


def render_template_for_user(user):
    """Docstring."""
    context = {}
    # give content login name and username
    logged_user = session['logname']
    context['logname'] = logged_user
    context['user_name'] = user

    logname_follows_username = False

    # check if logged use is following the user he is looking at
    conn = insta485.model.get_db()
    cur = conn.cursor()

    if logged_user != user:
        cur.execute(
            "SELECT * FROM following WHERE username1=? and username2=?",
            (logged_user, user))
        row = cur.fetchone()
        if row is None:
            logname_follows_username = False
        else:
            logname_follows_username = True
    context['logname_follows_username'] = logname_follows_username
    cur.execute("SELECT fullname FROM users where username=?", (user,))
    row = cur.fetchone()
    # this will only execute once, since logged_user will only have one
    #  fullname
    context['fullname'] = row['fullname']

    # how many people the user has followed
    count = 0
    cur.execute("SELECT * from following where username1=?", (user,))
    for row in cur:
        count += 1
    context['following'] = count

    # how many people followed the user
    count = 0
    cur.execute("SELECT * from following where username2=?", (user,))
    for row in cur:
        count += 1
    context['followers'] = count

    # the # of post the user has
    count = 0
    post_photo = []
    cur.execute("SELECT postid,filename from posts where owner=?", (user,))
    for row in cur:
        count += 1
        # the small image of post, click img leads to /p/<postid_url_slug>/
        temp = {}
        temp['post_id'] = row['postid']
        temp['img_url'] = "/uploads/" + row['filename']
        post_photo.append(temp)
    context['posts'] = post_photo
    context['total_posts'] = count

    return context


# print(render_template_for_user("awdeorio"))
@insta485.app.route('/u/<user>/', methods=['GET', 'POST'])
def show_user(user):
    """Docstring."""
    if request.method == 'GET':
        if 'logname' in session:
            context = render_template_for_user(user)
        else:
            return flask.redirect('/accounts/login/')
    else:

        conn = insta485.model.get_db()
        cur = conn.cursor()
        # this is a post request, will upload a file
        if 'create_post' in request.form:
            # Save POST request's file object to a temp file --
            #  provided by spec
            dummy, temp_filename = tempfile.mkstemp()
            file = flask.request.files["file"]
            file.save(temp_filename)

            # Compute filename
            hash_txt = sha256sum(temp_filename)
            dummy, suffix = os.path.splitext(file.filename)
            hash_filename_basename = hash_txt + suffix
            hash_filename = os.path.join(insta485.app.config["UPLOAD_FOLDER"],
                                         hash_filename_basename)

            # Move temp file to permanent location
            shutil.move(temp_filename, hash_filename)
            insta485.app.logger.debug("Saved %s", hash_filename_basename)

            # update sql
            # get how many post the user already have
            max_num = 0
            cur.execute("SELECT postid from posts")
            for row in cur:
                max_num = max(max_num, row["postid"])
            insert_num = max_num + 1
            # insert to sql(return current date and time)
            cur.execute(
                "INSERT INTO posts(postid, filename, owner) "
                "VALUES (?,?,?)",
                (insert_num, hash_filename_basename, user))
            conn.commit()
            context = render_template_for_user(user)
        # logged in user wants to follow current user he is looking at
        logged_user = session['logname']
        # follow and unfollow request
        if 'follow' in request.form:
            # update sql
            cur.execute(
                "INSERT INTO following(username1, username2) VALUES (?,?)",
                (logged_user, user))
            conn.commit()
            context = render_template_for_user(user)

        if 'unfollow' in request.form:
            cur.execute(
                "DELETE FROM following WHERE username1 =? AND username2=?",
                (logged_user, user))
            conn.commit()
            # after return, refresh the page, which means a new get request
            context = render_template_for_user(user)

    return flask.render_template('user.html', **context)


@insta485.app.route('/uploads/<imagename>')
def show_image(imagename):
    """Docstring."""
    return send_from_directory(insta485.app.config['UPLOAD_FOLDER'],
                               imagename, as_attachment=True)
