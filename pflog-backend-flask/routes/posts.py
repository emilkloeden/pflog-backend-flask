from flask import jsonify, abort, request
from peewee import IntegrityError
from playhouse.shortcuts import model_to_dict

from app import app
from auth import auth
from models import Comment, Post, User, DoesNotExist
from utils import slugify


@app.route("/posts", methods=["GET"])
def list_posts():
    posts = (
        Post.select(
            User.username,
            Post.title,
            Post.slug,
            Post.created_date,
            Post.published_date,
            Post.post_id,
            Post.body,
        )
        .join(User)
        .order_by(Post.published_date.desc())
        .dicts()
    )
    return jsonify(list(posts))


@app.route("/posts", methods=["POST"])
@auth.login_required(role="author")
def create_post():
    if not request.json:
        abort(400)
    Post.create(
        user=auth.current_user(),
        title=request.json["title"],
        slug=slugify(request.json["title"]),
        body=request.json["body"],
    )
    return "", 201


@app.route("/posts/<slug>", methods=["GET"])
def read_post(slug):
    return (
        Post.select(
            User.username,
            Post.title,
            Post.slug,
            Post.created_date,
            Post.published_date,
            Post.post_id,
            Post.body,
        )
        .join(User)
        .where(Post.slug == slug)
        .dicts()
        .get()
    )


@app.route("/posts/<slug>", methods=["PUT"])
@auth.login_required(role="author")
def update_post(slug):
    if not request.json:
        abort(400)
    if "title" not in request.json:
        abort(400)
    if "body" not in request.json:
        abort(400)

    try:
        post = Post.select().where(Post.slug == slug).get()
        if auth.current_user() != post.user:
            abort(403)
        title = request.json["title"]
        post.title = title
        post.body = request.json["body"]
        post.slug = slugify(title)
        post.save()
        post = (
            Post.select(
                User.username,
                Post.title,
                Post.slug,
                Post.created_date,
                Post.published_date,
                Post.post_id,
                Post.body,
            )
            .join(User)
            .where(Post.post_id == post.post_id)
            .dicts()
            .get()
        )
    except DoesNotExist:
        abort(404)
    return post, 201


@app.route("/posts/<slug>/comments", methods=["GET"])
def list_post_comments(slug):
    try:
        post = Post.select().where(Post.slug == slug).get()
        # TODO: Try to avoid n+1 here...
        return jsonify(
            [
                {
                    "username": comment.user.username,
                    "post": post.slug,
                    "comment": comment.comment,
                }
                for comment in post.comments
            ]
        )

    except DoesNotExist:
        abort(404)


@app.route("/posts/<slug>/comments", methods=["POST"])
@auth.login_required
def add_comment(slug):
    if not request.json:
        abort(400)
    if "comment" not in request.json:
        abort(400)
    try:
        post = Post.select().where(Post.slug == slug).get()
        comment = Comment(
            post=post, user=auth.current_user(), comment=request.json["comment"]
        )
        comment.save()
        return "", 201
    except DoesNotExist:
        abort(404)
