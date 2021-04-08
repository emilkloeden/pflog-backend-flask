from flask import abort, request
from werkzeug.security import check_password_hash, generate_password_hash
from peewee import IntegrityError
from playhouse.shortcuts import model_to_dict

from app import app
from models import User


@app.route("/users", methods=["POST"])
def create_user():
    required_fields = ["username", "first_name", "surname", "password", "email"]
    if not request.json:
        abort(400)

    elif not set(required_fields).issubset(set(request.json)):
        abort(400)
    try:
        r = request.json
        user = User(
            username=r["username"],
            first_name=r["first_name"],
            surname=r["surname"],
            password=generate_password_hash(r["password"]),
            email=r["email"],
        )
        user.save()

        dict_ = model_to_dict(user.get())
        del dict_["password"]

        return dict_, 201
    except IntegrityError:
        abort(409)

@app.route("/signin", methods=["POST"])
def signin():
    if not request.json:
        abort(400)

    elif "username" not in request.json or "password" not in request.json:
        abort(400)
    r = request.json
    user = User.select().where(
        User.username==r["username"]
    ).first()
    if not user:
        abort(400)
    if not check_password_hash(user.password, r["password"]):
        abort(400)
    return {"token": "token"}
