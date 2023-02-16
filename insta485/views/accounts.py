"""
Insta485 accounts view.

URLs include:
/
"""
import os
import uuid
import hashlib
import pathlib
import flask
import insta485
import insta485.views.index


@insta485.app.route('/accounts/login/')
def show_account_login():
    """Show login."""
    if 'username' not in flask.session:
        return flask.render_template("account_login.html")
    return flask.redirect(flask.url_for('show_index'))


@insta485.app.route('/accounts/logout/', methods=['POST'])
def show_account_logout():
    """Show log out."""
    flask.session.clear()
    return flask.redirect(flask.url_for('show_account_login'))


@insta485.app.route('/accounts/create/')
def show_account_create():
    """Show create."""
    if 'username' not in flask.session:
        return flask.render_template("account_create.html")
    return flask.redirect(flask.url_for('show_account_edit'))


@insta485.app.route('/accounts/delete/')
def show_account_delete():
    """Show delete."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_account_login'))
    return flask.render_template("account_delete.html",
                                 username=flask.session["username"])


@insta485.app.route('/accounts/edit/')
def show_account_edit():
    """Show edit."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for("show_account_login"))

    username = flask.session['username']
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT username, fullname, filename, email "
        "FROM users "
        "WHERE username == ? ",
        (username, )
    )
    row = cur.fetchall()[0]
    context = {
        "username": username,
        "pic_url": row["filename"],
        "fullname": row["fullname"],
        "email": row["email"],
    }
    return flask.render_template("account_edit.html", **context)


@insta485.app.route('/accounts/password/')
def show_account_password():
    """Show password."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for("show_account_login"))
    return flask.render_template("account_password.html")


# show account helper functions
def login_helper(username, password, connection):
    """Help login."""
    # connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT username, password "
        "FROM users "
        "WHERE username == ? ",
        (username, )
    )
    # If the username or password fields are empty, abort(400).
    if not username or not password:
        flask.abort(400)
    # If username and password authentication fails, abort(403).
    rows = cur.fetchall()
    if len(rows) == 0:
        flask.abort(403)
    # password match
    # get hashed password
    algorithm = 'sha512'
    # salt = uuid.uuid4().hex
    database_password = rows[0]['password']
    salt = database_password.split("$")[1]
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    if database_password != password_db_string:
        flask.abort(403)
    # Set a session cookie.
    flask.session['username'] = username
    # Redirect to URL.


def create_helper(username, password, email, fullname):
    """Help create account."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT username, password "
        "FROM users "
        "WHERE username == ? ",
        (username, )
    )
    rows = cur.fetchall()
    if len(rows) != 0:
        flask.abort(409)
    # create the hashed password
    password_db_string = hash_helper(password=password)

    # hash filename
    uuid_basename = hashing()

    cur = connection.execute(
        "INSERT INTO users "
        "(username, fullname, email, filename, password) "
        "VALUES (?, ?, ?, ?, ?) ",
        (username, fullname, email, uuid_basename, password_db_string)
    )


def edit_account_helper(connection, fullname, email):
    """Help edict account."""
    cur = connection.execute(
        "SELECT filename FROM users "
        "WHERE username == ?",
        (flask.session['username'], )
    )

    row = cur.fetchall()[0]
    filename = row['filename']

    # If no photo file is included, update only the user’s name and email.
    # Unpack flask object
    fileobj = flask.request.files["file"]
    if fileobj:
        # store the new photo
        new_filename = fileobj.filename
        stem = uuid.uuid4().hex
        suffix = pathlib.Path(new_filename).suffix.lower()
        uuid_basename = f"{stem}{suffix}"

        # Save to disk
        path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
        fileobj.save(path)
        path = 'var/uploads/'
        path = os.path.join(path, filename)
        os.remove(path)

        filename = uuid_basename

    cur = connection.execute(
        "UPDATE users "
        "set fullname = ?, email = ?, filename = ? "
        "WHERE username = ?",
        (fullname, email, filename, flask.session['username'])
    )


def hash_helper(password):
    """Take in a passsord and returned a hashed string."""
    algorithm = 'sha512'
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    return password_db_string


def update_password_helper(connection, password, new1, new2):
    """Help update password."""
    cur = connection.execute(
        "SELECT username, password "
        "FROM users "
        "WHERE username == ? ",
        (flask.session['username'], )
    )
    rows = cur.fetchall()

    algorithm = 'sha512'
    database_password = rows[0]['password']
    salt = database_password.split("$")[1]
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    if rows[0]['password'] != password_db_string:
        flask.abort(403)
    if new1 != new2:
        flask.abort(401)

    # update the new password
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + new1
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    new_password = "$".join([algorithm, salt, password_hash])
    print("new")
    print(new_password)
    cur = connection.execute(
        "UPDATE users "
        "SET password = ? "
        "WHERE username == ? ",
        (new_password, flask.session['username'], )
    )


@insta485.app.route('/accounts/', methods=['POST'])
def show_account():
    """Show account."""
    operation = flask.request.form.get('operation')
    connection = insta485.model.get_db()
    if operation == 'login':
        username = flask.request.form.get('username')
        password = flask.request.form.get('password')
        login_helper(username=username, password=password,
                     connection=connection)
        if flask.request.args.get('target') is None:
            return flask.redirect('/')
        return flask.redirect(flask.request.args.get('target'))

    if operation == 'create':
        username = flask.request.form.get('username')
        password = flask.request.form.get('password')
        fullname = flask.request.form.get('fullname')
        email = flask.request.form.get('email')
        # file = flask.request.form.get('file')
        if ('file' not in flask.request.files) or \
           (not (username and password and fullname and email)):
            flask.abort(400)
        # fileobj = flask.request.files["file"]
        # If any of the above fields are empty, abort(400).
        # if not (username and password and fullname and email):
        #     flask.abort(400)
        # If a user tries to create an account with an
        # existing username in the database
        create_helper(username=username, password=password,
                      email=email, fullname=fullname)

        # Set a session cookie.
        flask.session['username'] = username

        return flask.redirect(flask.request.args.get('target'))

    if operation not in ('login', 'create'):
        # if not flask.session['username']:
        #     flask.abort(403)
        if 'username' not in flask.session:
            flask.abort(403)

    if operation == 'delete':
        # if not flask.session['username']:
        #     flask.abort(403)
        # if 'username' not in flask.session:
        #     flask.abort(403)

        # Delete all post files created by this user.
        cur = connection.execute(
            "SELECT filename FROM posts "
            "WHERE owner == ?",
            (flask.session['username'], )
        )
        post_files = cur.fetchall()
        for post_file in post_files:
            path = 'var/uploads/'
            path = os.path.join(path, post_file['filename'])
            os.remove(path)

        # Delete user icon file.
        cur = connection.execute(
            "SELECT filename FROM users "
            "WHERE username == ?",
            (flask.session['username'], )
        )
        profile_pic = cur.fetchall()
        path = 'var/uploads/'
        path = os.path.join(path, profile_pic[0]['filename'])
        os.remove(path)

        # Delete all related entries in all tables.
        cur = connection.execute(
            "DELETE FROM users "
            "WHERE username == ? ",
            (flask.session['username'], )
        )

        flask.session.clear()
        # return flask.redirect(flask.request.args.get('target'))

    if operation == 'edit_account':
        # if not flask.session['username']:
        #     flask.abort(403)
        fullname = flask.request.form.get('fullname')
        email = flask.request.form.get('email')

        if not (fullname and email):
            flask.abort(400)

        edit_account_helper(connection=connection,
                            fullname=fullname, email=email)
        # return flask.redirect(flask.request.args.get('target'))

    if operation == 'update_password':
        # if not flask.session['username']:
        #     flask.abort(403)

        password = flask.request.form.get('password')
        new_password1 = flask.request.form.get('new_password1')
        new_password2 = flask.request.form.get('new_password2')

        # If any of the above fields are empty, abort(400).
        if not (password and new_password1 and new_password2):
            flask.abort(400)

        # Verify password against the user’s password hash in the database
        update_password_helper(connection=connection,
                               password=password,
                               new1=new_password1,
                               new2=new_password2)
        # return flask.redirect(flask.request.args.get('target'))

    return flask.redirect(flask.request.args.get('target'))


def hashing():
    """Help hashing."""
    # store the file in the os system Unpack flask object
    fileobj = flask.request.files["file"]
    filename = fileobj.filename
    # Compute base name (filename without directory).
    stem = uuid.uuid4().hex
    suffix = pathlib.Path(filename).suffix.lower()
    uuid_basename = f"{stem}{suffix}"
    # Save to disk
    path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
    fileobj.save(path)
    return uuid_basename


def basic_auth():
    """Authenticate."""
    if flask.request.authorization is None:
        return False

    connection = insta485.model.get_db()
    username = flask.request.authorization['username']
    password = flask.request.authorization['password']
    cur = connection.execute(
        "SELECT username, password FROM users "
        "WHERE username == ? ",
        (username, )
    )
    # If username and password authentication fails.
    rows = cur.fetchall()
    if len(rows) == 0:
        return False
    # password match
    # get hashed password
    algorithm = 'sha512'
    database_password = rows[0]['password']
    salt = database_password.split("$")[1]
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    if database_password != password_db_string:
        return False
    return True
