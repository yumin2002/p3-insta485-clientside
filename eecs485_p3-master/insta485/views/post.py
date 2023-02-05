"""
Insta485 post (main) view.

URLs include:
/
"""
import os
import arrow
import flask
from flask import request, session
import insta485
import insta485.model
import insta485.config


def render_template_for_post(post_id):
    """Docstring."""
    context = {}
    context['no_logname'] = False
    context['message'] = ''
    if 'logname' not in session:
        context['no_logname'] = True
        return context

    context['desplay_delete_button'] = False
    context['logname'] = session['logname']
    context['postid'] = post_id
    context['login_user_liked_the_post'] = False

    conn = insta485.model.get_db()
    cor = conn.cursor()
    cor.execute("SELECT owner,filename, created from posts WHERE postid=?",
                (post_id,))

    row = cor.fetchone()
    if row is None:
        context = {'message': 'Not Found', 'status_code': 404}
        return context

    context['owner'] = row['owner']

    if context['owner'] == session['logname']:
        context['desplay_delete_button'] = True

    # get the posted image
    context['img_url'] = "/uploads/" + row['filename']
    # print(context['img_url'])

    # convert to human readable format -- get this idea from piazza @840
    context['timestamp'] = arrow.get(row['created']).humanize()

    # get the owner's profile picture
    cor.execute("SELECT filename from users WHERE username=?",
                (context['owner'],))
    row = cor.fetchone()
    owner_img_url = row['filename']
    # print(owner_img_url)
    context['owner_img_url'] = "/uploads/" + owner_img_url
    # print(context['owner_img_url'])

    # count the number of likes of a post
    cor.execute("SELECT * from likes WHERE postid=?", (post_id,))
    context['likes'] = len(cor.fetchall())

    # all the comments for the specific post id
    comments = []
    cor.execute("SELECT owner,text,commentid from comments WHERE postid=?",
                (post_id,))
    for row in cor:
        temp = {}
        temp['owner'] = row['owner']
        temp['text'] = row['text']
        temp['commentid'] = row['commentid']
        comments.append(temp)

    context['comments'] = comments

    cor.execute("SELECT * from likes WHERE owner=? AND postid=?",
                (session['logname'], post_id))
    if cor.fetchone():
        context['login_user_liked_the_post'] = True
    return context


@insta485.app.route('/p/<post_id>/', methods=['GET', 'POST'])
def show_post(post_id):
    """Docstring."""
    # like, unlike, comment, uncomment, delete the post
    if request.method == 'GET':
        if 'logname' in session:
            context = render_template_for_post(post_id)
            return flask.render_template('post.html', **context)
        return flask.redirect('/accounts/login/')

    conn = insta485.model.get_db()
    cor = conn.cursor()

    if 'like' in request.form:
        cor.execute("INSERT INTO likes(owner,postid) VALUES (?,?)",
                    (session["logname"], post_id))
        conn.commit()

    elif 'unlike' in request.form:
        cor.execute("DELETE FROM likes WHERE owner=? AND postid=?",
                    (session["logname"], post_id))
        conn.commit()

    elif 'comment' in request.form:
        max_comment_id = 0
        cor.execute("SELECT commentid FROM comments")
        for row in cor:
            max_comment_id = max(max_comment_id, row['commentid'])
        max_comment_id += 1
        cor.execute(
            "INSERT INTO comments(commentid,owner,postid,text) "
            "VALUES (?,?,?,?)",
            (max_comment_id, session["logname"], post_id,
             request.form['text']))
        conn.commit()

    # delete comment
    elif 'uncomment' in request.form:
        cor.execute("DELETE FROM comments WHERE commentid=?",
                    (request.form["commentid"],))
        conn.commit()

    # delete post
    else:
        # first, delete the post file image
        cor.execute("SELECT filename FROM posts WHERE postid=?",
                    (post_id,))
        for row in cor:
            os.remove(
                insta485.config.UPLOAD_FOLDER + "/" + row['filename'])
            break
        # second, delete the post info that is stored in the data base
        cor.execute("DELETE FROM posts WHERE postid=?", (post_id,))
        cor.execute("DELETE FROM likes WHERE postid=?", (post_id,))
        cor.execute("DELETE FROM comments WHERE postid=?", (post_id,))
        conn.commit()
        return flask.redirect('/')

    context = render_template_for_post(post_id)
    return flask.render_template('post.html', **context)
