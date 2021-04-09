import jwt
from datetime import datetime, timedelta
from flask import abort, request, make_response, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from peewee import IntegrityError
from playhouse.shortcuts import model_to_dict

from app import app
from auth import auth
from tokenauth import token_required
from models import User


@app.route("/user", methods=["GET"])
@token_required
def get_user(current_user):
    user_roles = [
        model_to_dict(user_role.role)["role"] for user_role in current_user.user_roles
    ]
    print(user_roles)
    dict_ = model_to_dict(current_user)
    dict_["is_admin"] = "admin" in user_roles
    dict_["is_author"] = "author" in user_roles
    del dict_["password"]
    return dict_


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

        token = jwt.encode(
            {
                "username": user.username,
                "exp": datetime.utcnow() + timedelta(minutes=30),
            },
            app.config["SECRET_KEY"],
        )
        return make_response(jsonify({"token": token.decode("UTF-8")}), 201)
    except IntegrityError:
        abort(409)


@app.route("/signin", methods=["POST"])
def signin():
    if not request.json:
        abort(400)

    elif "username" not in request.json or "password" not in request.json:
        abort(400)
    r = request.json
    user = User.select().where(User.username == r["username"]).first()
    if not user:
        abort(400)
    if not check_password_hash(user.password, r["password"]):
        abort(400)
    token = jwt.encode(
        {"username": user.username, "exp": datetime.utcnow() + timedelta(minutes=30)},
        app.config["SECRET_KEY"],
    )
    return make_response(jsonify({"token": token.decode("UTF-8")}), 200)
