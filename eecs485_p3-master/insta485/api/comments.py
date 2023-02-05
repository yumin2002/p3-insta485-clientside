"""REST API for comments."""
import flask
import insta485


def create_context(postid_url_slug):
    """Create context for comments."""
    db_comments = insta485.model.get_db()
    cursor = db_comments.cursor()
    context = {}

    # post
    postid = postid_url_slug

    # comments
    comments = []
    for data in cursor.execute("SELECT * FROM comments WHERE postid=?",
                               (postid,)):
        comment = {}
        comment['commentid'] = data['commentid']
        comment['owner'] = data['owner']
        comment['owner_show_url'] = '/u/' + data['owner'] + '/'
        comment['postid'] = data['postid']
        comment['text'] = data['text']
        comments.append(comment)
    context['comments'] = comments

    # url
    context['url'] = flask.request.path

    return context


@insta485.app.route('/api/v1/p/<int:postid_url_slug>/comments/',
                    methods=['GET', 'POST'])
def get_comments(postid_url_slug):
    """Return a list of comments for one post."""
    if flask.request.method == 'POST':
        if 'logname' not in flask.session:
            context = {}
            context['message'] = "Not Found"
            context['status_code'] = 403
            return flask.jsonify(**context), 403

        db_post = insta485.model.get_db()
        cursor = db_post.cursor()
        cursor.execute("SELECT * FROM posts WHERE postid=?",
                       (postid_url_slug,))
        data = cursor.fetchone()
        if data is None:
            context = {}
            context['message'] = "Not Found"
            context['status_code'] = 404
            return flask.jsonify(**context), 404

        context = {}
        max_comment_id = 0
        cursor.execute("SELECT * FROM comments")
        for row in cursor:
            max_comment_id = max(max_comment_id, row['commentid'])
        max_comment_id += 1
        cursor.execute(
            "INSERT INTO comments(commentid,owner,postid,text) "
            "VALUES (?,?,?,?)",
            (max_comment_id, flask.session["logname"], postid_url_slug,
             flask.request.json.get('text')))

        context['commentid'] = max_comment_id
        context['owner'] = flask.session["logname"]
        context['owner_show_url'] = '/u/' + flask.session["logname"] + '/'
        context['postid'] = postid_url_slug
        context['text'] = flask.request.json.get('text')

        return flask.jsonify(**context), 201

    if 'logname' not in flask.session:
        return flask.redirect('/accounts/login/', code=302)

    db_get = insta485.model.get_db()
    cursor = db_get.cursor()
    cursor.execute("SELECT * FROM posts WHERE postid=?",
                   (postid_url_slug,))
    valid = cursor.fetchone()
    if valid is None:
        error = {}
        error['message'] = "Not Found"
        error['status_code'] = 404
        return flask.jsonify(**error), 404

    context = create_context(postid_url_slug)
    return flask.jsonify(**context)
