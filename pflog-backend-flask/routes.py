from flask import render_template, jsonify, abort, request, make_response

from app import app
from models import User, Post
from utils import slugify


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({"error": "Bad request"}), 400)


@app.route("/")
def home_page():
    # TODO: See if we can serve the index.html that
    # the Frontend will require from the API server

    # return render_template('index.html')
    posts = Post.select().order_by(Post.published_date.desc()).dicts()

    return jsonify(list(posts))


@app.route("/posts", methods=["GET", "POST"])
def create_post():
    if request.method == "GET":
        posts = Post.select().order_by(Post.published_date.desc()).dicts()
        return jsonify(list(posts))
    if not request.json:
        abort(400)
    else:
        user = User.get(User.id == 1)
        print(user.first_name)

        Post.create(
            user=user,
            title=request.json["title"],
            slug=slugify(request.json["title"]),
            body=request.json["body"],
        )
        return "", 201


@app.route("/posts/<slug>", methods=["GET", "PUT"])
def read_or_update_post(slug):
    if request.method == "GET":
        return Post.select().where(Post.slug == slug).dicts().get()
    else:
        if not request.json:
            abort(400)
        if "title" not in request.json:
            abort(400)
        if "body" not in request.json:
            abort(400)

        post = Post.select().where(Post.slug == slug).get()
        title = request.json["title"]
        post.title = title
        post.body = request.json["body"]
        post.slug = slugify(title)
        post.save()
        post = Post.select().where(Post.post_id == post.post_id).dicts().get()
    return post, 201
