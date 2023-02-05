"""
Insta485 index (main) view.

URLs include:
/
"""
import flask
import arrow

import insta485


def create_context():
    """Docstring."""
    database = insta485.model.get_db()
    cursor = database.cursor()
    context = {}
    context['logname'] = flask.session['logname']
    # get a list of people followed by current use
    following = []
    following.append(flask.session['logname'])
    for follow in cursor.execute("SELECT * FROM following WHERE username1=?",
                                 (flask.session['logname'],)):
        following.append(follow['username2'])

    # parse all posts
    post_collection = []
    for post in cursor.execute("SELECT * FROM posts"):
        if post['owner'] in following:
            post_collection.append(post)
    post_collection.reverse()

    # put every post in posts
    posts = []
    for post in post_collection:
        info = {}
        # postid, owner, timestamp, img_url from post
        info['postid'] = post['postid']
        info['owner'] = post['owner']
        info['timestamp'] = arrow.get(post['created']).humanize()
        info['img_url'] = '/uploads/' + post['filename']

        # owner image url
        for data in cursor.execute("SELECT * FROM users WHERE username=?",
                                   (post['owner'],)):
            info['owner_img_url'] = '/uploads/' + data['filename']

        # likes
        info['logname_liked_post'] = False
        count = 0
        for like in cursor.execute("SELECT * FROM likes WHERE postid=?",
                                   (post['postid'],)):
            count += 1
            if like['owner'] == flask.session['logname']:
                info['logname_liked_post'] = True
        info['likes'] = count

        # comment
        comments = []
        comment_collection = []
        for data in cursor.execute("SELECT * FROM comments WHERE postid=?",
                                   (info['postid'],)):
            comment_collection.append(data)
        for data in comment_collection:
            comment = {}
            comment['owner'] = data['owner']
            comment['text'] = data['text']
            comments.append(comment)
        info['comments'] = comments
        posts.append(info)

    context['posts'] = posts
    return context


@insta485.app.route('/', methods=['GET', 'POST'])
def show_index():
    """Display / route."""
    if flask.request.method == 'POST':
        if 'logname' not in flask.session:
            flask.abort(403)
        database = insta485.model.get_db()
        cursor = database.cursor()
        if 'like' in flask.request.form:
            cursor.execute("INSERT INTO likes (owner, postid) VALUES (?,?)", (
                flask.session['logname'], flask.request.form['postid']))
        if 'unlike' in flask.request.form:
            cursor.execute("DELETE FROM likes WHERE owner=? AND postid=?", (
                flask.session['logname'], flask.request.form['postid']))
        if 'comment' in flask.request.form:
            max_comment_id = 0
            for row in cursor.execute("SELECT * FROM comments"):
                max_comment_id = max(max_comment_id, row['commentid'])
            max_comment_id += 1
            cursor.execute(
                "INSERT INTO comments (commentid, owner, postid, text) "
                "VALUES (?,?,?,?)", (max_comment_id, flask.session['logname'],
                                     flask.request.form['postid'],
                                     flask.request.form['text']))
        database.commit()
    else:
        if 'logname' not in flask.session:
            return flask.redirect('/accounts/login/', code=302)

    context = create_context()
    return flask.render_template('index.html', **context)
