from flask import jsonify, request, url_for, current_app, g

from app import db
from app.decorators import permission_required
from app.models import Post, Permission
from . import api

@api.route('/posts')
def get_posts():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_posts', page=page-1, _external= True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_posts', page=page+1, _external= True)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })

@api.route('/posts/<int:id>')
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify(post.to_json())

#http --auth  wuhan:aa --json POST http://127.0.0.1:5000/api/v1/posts "body=add a post from cmd"
@api.route('/posts', methods=['POST'])
# @permission_required(Permission.WRITE)
def new_post():
    post = Post.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json()), 201, \
        {'Location': url_for('api.get_post', id=post.id)}
