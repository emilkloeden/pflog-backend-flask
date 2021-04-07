from flask import jsonify, abort, request
from peewee import IntegrityError

from app import app
from auth import auth
from models import User, UserRole, Role


@app.route("/user-roles", methods=["GET"])
@auth.login_required(role="admin")
def list_user_roles():
    users = (
        User.select(User.username, Role.role)
        .join(UserRole)
        .join(Role)
        .dicts()
        .order_by(User.username)
    )
    return jsonify(list(users))


@app.route("/user-roles", methods=["POST"])
@auth.login_required(role="admin")
def add_user_role():
    if not request.json:
        abort(400)
    elif "username" not in request.json:
        abort(400)
    elif "role" not in request.json:
        abort(400)
    else:
        print(request.json)
        user = User.select().where(User.username == request.json["username"]).first()
        print(user)
        role = Role.select().where(Role.role == request.json["role"]).first()
        print(role)
        if not user or not role:
            abort(400)
        else:
            try:
                user_role = UserRole(user=user, role=role)
                user_role.save()

                return "", 201
            except IntegrityError:
                abort(400)