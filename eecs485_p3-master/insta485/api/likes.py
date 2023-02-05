"""REST API for likes."""
import flask
from flask import jsonify
import insta485


@insta485.app.route('/api/v1/p/<postid>/likes/',
                    methods=['GET', 'POST', 'DELETE'])
def get_likes(postid):
    """Docstring func."""
    context = insta485.views.post.render_template_for_post(postid)
    if context['message'] == 'Not Found':
        return jsonify(**context), 404

    if context['no_logname'] is True:
        not_login = {}
        not_login['message'] = "Forbidden"
        not_login['status_code'] = 403
        return jsonify(not_login), 403

    database = insta485.model.get_db()
    cursor = database.cursor()
    if flask.request.method == 'GET':
        get_like = {}
        get_like["likes_count"] = context['likes']
        get_like["logname_likes_this"] = context['login_user_liked_the_post']
        get_like["postid"] = int(postid)
        get_like["url"] = "/api/v1/p/" + postid + '/likes/'
        return jsonify(**get_like)

    if flask.request.method == 'POST':
        create_like = {}
        create_like["logname"] = context['logname']
        create_like["postid"] = int(postid)

        if context['login_user_liked_the_post']:
            create_like["message"] = "Conflict"
            create_like["status_code"] = 409
            return jsonify(create_like), 409
        cursor.execute("INSERT INTO likes (owner, postid) VALUES (?,?)", (
            flask.session['logname'], postid))
        return jsonify(**create_like), 201

    cursor.execute("DELETE FROM likes WHERE owner=? AND postid=?", (
        flask.session['logname'], postid))
    return jsonify(), 204
