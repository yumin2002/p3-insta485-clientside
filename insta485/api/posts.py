"""REST API for posts."""
import flask
import insta485
import insta485.views.accounts


@insta485.app.route('/api/v1/')
def get_service():
    """Show availables service."""
    context = {
        "comments": "/api/v1/comments/",
        "likes": "/api/v1/likes/",
        "posts": "/api/v1/posts/",
        "url": "/api/v1/"
    }
    return flask.jsonify(**context)


@insta485.app.route('/api/v1/posts/')
def get_posts():
    """Get the posts."""
    # authenticatisouon
    auth = insta485.views.accounts.basic_auth()
    if 'username' not in flask.session and not auth:
        flask.abort(403)

    # variables & set page and size
    connection = insta485.model.get_db()
    logname = ""
    if flask.request.authorization is not None:
        logname = flask.request.authorization["username"]
    else:
        logname = flask.session["username"]
    url = flask.request.url.removeprefix("http://localhost")
    size = flask.request.args.get("size", default=10, type=int)
    page = flask.request.args.get("page", default=0, type=int)

    # set default postid_lte or get the query parameter postid_lte
    cur = connection.execute(
        "SELECT postid FROM posts "
        "WHERE owner IN "
        "(SELECT username2 FROM following WHERE (username1 == ?)) "
        "OR (owner == ? ) "
        "ORDER BY postid DESC "
        "LIMIT 1",
        (logname, logname)
    )
    default_postid = cur.fetchall()
    if len(default_postid) == 0:
        context = {
            "next": "",
            "results": [],
            "url": url
        }
        return flask.jsonify(**context)
    postid_lte = flask.request.args.get(
        "postid_lte", default=default_postid[0]["postid"], type=int)

    # Bad request for invalid parameter
    if (size < 0) or (page < 0) or (postid_lte < 0):
        flask.abort(400)

    # set results: find the posts of current page
    cur = connection.execute(
        "SELECT postid, filename, owner, created FROM posts "
        "WHERE owner IN "
        "(SELECT username2 FROM following WHERE (username1 == ?)) "
        "OR (owner == ? ) "
        "AND postid <= ? "
        "ORDER BY postid DESC "
        "LIMIT ? OFFSET ?",
        (logname, logname, postid_lte, size, size*page)
    )
    result = []
    posts = cur.fetchall()
    for post in posts:
        result.append({
                      "postid": post["postid"],
                      "url": f'/api/v1/posts/{post["postid"]}/'
                      })

    # set next:
    # if all result can be displayed in current page
    # then no next page
    # otherwise, has next page
    next_url = ''
    cur = connection.execute(
        "SELECT postid FROM posts "
        "WHERE owner IN "
        "(SELECT username2 FROM following WHERE (username1 == ?)) "
        "OR (owner == ? ) "
        "AND postid <= ? "
        "ORDER BY postid DESC ",
        (logname, logname, postid_lte)
    )
    total_posts = len(cur.fetchall())
    if total_posts < size*(page+1):
        next_url = ''
    else:
        next_url = \
            f"/api/v1/posts/?size={size}&page={page+1}&postid_lte={postid_lte}"

    # return
    context = {
        "next": next_url,
        "results": result,
        "url": url
    }
    return flask.jsonify(**context)


@insta485.app.route('/api/v1/posts/<postid>/')
def get_post(postid):
    """Get the posts."""
    # authentication
    if 'username' not in flask.session \
            and not insta485.views.accounts.basic_auth():
        flask.abort(403)

    # variables & set page and size
    connection = insta485.model.get_db()
    logname = ""
    if flask.request.authorization is not None:
        logname = flask.request.authorization["username"]
    else:
        logname = flask.session["username"]

    # comments
    cur = connection.execute(
        "SELECT commentid, owner, text FROM comments "
        "WHERE postid = ? ",
        (int(postid), )
    )
    comments = cur.fetchall()
    for comment in comments:
        comment["lognameOwnsThis"] = (logname == comment["owner"])
        comment["ownerShowUrl"] = f'/users/{comment["owner"]}/'
        comment['url'] = f'/api/v1/comments/{comment["commentid"]}/'
    # comments_url = f"/api/v1/comments/?postid={postid}"

    cur = connection.execute(
        "SELECT created, filename, owner FROM posts "
        "WHERE postid = ? ",
        (int(postid), )
    )
    post = cur.fetchall()

    # error: post does not exist
    if len(post) == 0:
        flask.abort(404)

    # get post info
    created = post[0]["created"]
    img_url = f'/uploads/{post[0]["filename"]}'

    # check likes
    cur = connection.execute(
        "SELECT likeid FROM likes "
        "WHERE postid = ?",
        (postid, )
    )
    num_likes = len(cur.fetchall())
    cur = connection.execute(
        "SELECT likeid FROM likes "
        "WHERE postid = ? AND owner = ?",
        (int(postid), logname, )
    )
    logname_like = cur.fetchall()
    logname_likes_this = False
    like_url = None
    if len(logname_like) != 0:
        logname_likes_this = True
        like_url = f'/api/v1/likes/{logname_like[0]["likeid"]}/'

    # owner info
    owner = post[0]["owner"]
    cur = connection.execute(
        "SELECT filename FROM users "
        "WHERE username = ?",
        (owner, )
    )
    # filename = cur.fetchall()[0]["filename"]
    # ownerImgUrl = f'/uploads/{filename}'
    # ownerShowUrl = f'/users/{owner}/'
    # postShowUrl = f'/posts/{postid}/'
    # postid = int(postid)
    # url = f'/api/v1/posts/{postid}/'
    context = {
        "comments": comments,
        "comments_url": f"/api/v1/comments/?postid={postid}",
        "created": created,
        "imgUrl": img_url,
        "likes": {
            "lognameLikesThis": logname_likes_this,
            "numLikes": num_likes,
            "url": like_url
        },
        "owner": owner,
        "ownerImgUrl": f'/uploads/{cur.fetchall()[0]["filename"]}',
        "ownerShowUrl": f'/users/{owner}/',
        "postShowUrl": f'/posts/{postid}/',
        "postid": int(postid),
        "url": f'/api/v1/posts/{postid}/'
    }
    return flask.jsonify(**context)


@insta485.app.route('/api/v1/comments/', methods=["POST"])
def post_comment():
    """Update the comments on a post."""
    print("Entered post comment")

    auth = insta485.views.accounts.basic_auth()
    if 'username' not in flask.session and not auth:
        flask.abort(403)
    print("Entered post comment1")
    postid = flask.request.args.get('postid')

    comment_text = flask.request.json['text']
    print("Entered post comment2")
    connection = insta485.model.get_db()

    if flask.request.authorization is not None:
        logname = flask.request.authorization["username"]
    else:
        logname = flask.session["username"]

    # insert the comment into db
    cur = connection.execute(
        "INSERT INTO comments (owner, postid, text) VALUES (?, ?, ?) ",
        (logname, postid, comment_text)
    )

    # retrieve the comment for the json
    cur = connection.execute(
        "SELECT last_insert_rowid() FROM comments "
    )
    commentid = cur.fetchall()[0]["last_insert_rowid()"]
    # need to check if logname owns?
    context = {
        "commentid": commentid,
        "lognameOwnsThis": True,
        "owner": logname,
        "ownerShowUrl": f"/users/{logname}/",
        "text": comment_text,
        "url": f"/api/v1/comments/{postid}/"
    }
    print("Entered post comment3")
    return flask.jsonify(**context), 201


@insta485.app.route('/api/v1/comments/<commentid>/', methods=["DELETE"])
def delete_comment(commentid):
    """Update the comments on a post."""
    print("entered delete comment")

    auth = insta485.views.accounts.basic_auth()
    connection = insta485.model.get_db()
    # if 'username' not in flask.session and not auth:
    #     flask.abort(403)
    # if flask.request.authorization is not None:
    #     logname = flask.request.authorization["username"]
    # else:
    #     logname = flask.session["username"]
    logname = assign_logname(auth)

    cur = connection.execute(
        "SELECT owner, commentid FROM comments WHERE commentid == ? ",
        (commentid, )
    )
    comment_to_delete = cur.fetchall()
    # If the commentid does not exist, return 404.
    if len(comment_to_delete) == 0:
        flask.abort(404)
    # If the user doesn’t own the comment, return 403.
    if comment_to_delete[0]['owner'] != logname:
        flask.abort(403)

    # delete the comment from db
    cur = connection.execute(
        "DELETE FROM comments WHERE commentid == ? ",
        (commentid, )
    )

    return "", 204


def assign_logname(auth):
    """assign_logname."""
    if 'username' not in flask.session and not auth:
        flask.abort(403)
    if flask.request.authorization is not None:
        return flask.request.authorization["username"]
    return flask.session["username"]
