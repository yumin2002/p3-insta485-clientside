"""REST API for post."""
import flask
from flask import jsonify
import insta485


# GET	/api/v1/	Return API resource URLs
@insta485.app.route('/api/v1/', methods=['GET'])
def get_services():
    """docstring."""
    if 'logname' not in flask.session:
        context = {'message': 'Forbidden', 'status_code': 403}
        return jsonify(context), 403
    context = {"posts": "/api/v1/p/", "url": "/api/v1/"}
    return jsonify(**context)


@insta485.app.route('/api/v1/p/', methods=['GET'])
def get_post_list():
    """docstring."""
    # GET	/api/v1/p/	Return 10 newest posts
    # GET	/api/v1/p/?size=N	Return N newest posts
    # GET	/api/v1/p/?page=N	Return N’th page of posts
    # {
    #  "posts": "/api/v1/p/",
    #  "url": "/api/v1/"
    # }

    if 'logname' not in flask.session:
        context = {'message': 'Forbidden', 'status_code': 403}
        return jsonify(**context), 403

    context = {"url": "/api/v1/p/"}
    size = flask.request.args.get("size", default=10, type=int)
    page = flask.request.args.get("page", default=0, type=int)
    if size < 0 or page < 0:
        context = {"message": "Bad Request", "status_code": 400}
        return jsonify(**context), 400
    results = []
    conn = insta485.model.get_db()
    cor = conn.cursor()
    # print(flask.session['logname'], size * page, size)
    cor.execute(
        "SELECT postid from posts where owner=? or owner in "
        "(select username2 from following where username1=?) "
        "order by postid desc limit ? offset ?",
        (flask.session['logname'], flask.session['logname'],
         size + 1, size * page))
    for row in cor:
        post_id = row['postid']
        record = {"postid": post_id, "url": "/api/v1/p/%d/" % post_id}
        results.append(record)
    if len(results) > size:
        context["results"] = results[:size]
        context["next"] = "/api/v1/p/?size=%d&page=%d" % (size, page + 1)
    else:
        context["results"] = results
        context["next"] = ""
    cor.close()
    # print(context)
    return jsonify(**context)


@insta485.app.route('/api/v1/p/<int:postid>/', methods=['GET'])
def get_post(postid):
    """docstring."""
    if 'logname' not in flask.session:
        context = {'message': 'Forbidden', 'status_code': 403}
        return jsonify(**context), 403

    context = {}
    context["url"] = "/api/v1/p/%d/" % postid
    context["post_show_url"] = "/p/%d/" % postid
    conn = insta485.model.get_db()
    cor = conn.cursor()
    cor.execute("SELECT owner,filename, created from posts WHERE postid=?",
                (postid,))
    row = cor.fetchone()
    if row is None:
        context = {'message': 'Not Found', 'status_code': 404}
        return jsonify(**context), 404
    context["owner"] = row["owner"]
    context["owner_show_url"] = "/u/%s/" % row["owner"]
    context["img_url"] = "/uploads/" + row['filename']
    context["age"] = row["created"]

    cor.execute("SELECT filename from users WHERE username=?",
                (row['owner'],))
    row = cor.fetchone()
    owner_img_url = row['filename']
    # print(owner_img_url)
    context['owner_img_url'] = "/uploads/" + owner_img_url
    # print(context['owner_img_url'])

    return jsonify(**context)
