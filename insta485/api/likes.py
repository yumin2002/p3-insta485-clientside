"""REST API for likes."""
import flask
import insta485
from insta485.views.accounts import basic_auth


@insta485.app.route('/api/v1/likes/', methods=["POST"])
def post_like():
    """Post likes."""
    print("in post like")
    auth = basic_auth()
    if not auth and 'username' not in flask.session:
        print("exit1")
        flask.abort(403)
    # get logname
    if flask.request.authorization is not None:
        logname = flask.request.authorization["username"]
    # elif flask.request.authorization is None:
    #     print("exit2")
    #     flask.abort(403)
    else:
        logname = flask.session["username"]
    print(flask.request.args.get('postid'))
    postid = int(flask.request.args.get('postid'))

    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT likeid FROM likes "
        "WHERE owner=? AND postid=?",
        (logname, postid, )
    )
    rows = cur.fetchall()

    if len(rows) != 0:
        likeid = rows[0]['likeid']
        data = {
            "likeid": likeid,
            "url": f"/api/v1/likes/{likeid}/"
        }
        return flask.jsonify(data)
    print("debug")
    print(postid)
    print(logname)
    cur = connection.execute(
        "INSERT INTO likes (owner, postid)"
        "VALUES (?, ?)",
        (logname, postid)
    )

    # get likeid
    cur = connection.execute(
        "SELECT likeid FROM likes "
        "WHERE owner=? AND postid=?",
        (logname, postid, )
    )
    rows = cur.fetchall()
    likeid = rows[0]['likeid']

    data = {
        "likeid": likeid,
        "url": f"/api/v1/likes/{likeid}/"
    }
    return flask.jsonify(**data), 201


@insta485.app.route('/api/v1/likes/<likeid>/', methods=["DELETE"])
def delete_like(likeid):
    """Delete likes."""
    auth = basic_auth()
    logname = ""

    if not auth and 'username' not in flask.session:
        flask.abort(403)

    if flask.request.authorization is not None:
        logname = flask.request.authorization["username"]
    else:
        logname = flask.session["username"]

    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT owner from likes "
        "WHERE likeid=? ",
        (int(likeid), )
    )

    rows = cur.fetchall()

    if len(rows) != 0:
        # If the user does not own the like, return 403.
        if logname != rows[0]['owner']:
            return "", 403
        cur = connection.execute(
            "DELETE FROM likes "
            "WHERE likeid=?",
            (int(likeid),)
        )
        return "", 204

    # If the likeid does not exist, return 404.
    return "", 404
