import jwt
from functools import wraps, partial
from flask import request, abort

from app import app
from models import Role, User, UserRole


def token_required(fn=None, *, role=None):
    if fn is None:
        return partial(token_required, role=role)

    @wraps(fn)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
        if not token:
            abort(401)

        try:
            token_string = token.replace("Bearer ", "")
            data = jwt.decode(token_string, app.config["SECRET_KEY"])
            if role is None:
                current_user = (
                    User.select().where(User.username == data["username"]).first()
                )
            else:
                current_user = (
                    User.select()
                    .join(UserRole)
                    .join(Role)
                    .where(User.username == data["username"])
                    .where(Role.role == role)
                    .first()
                )
        except Exception as e:
            print(e)
            abort(401)
        try:
            return fn(current_user, *args, **kwargs)
        except TypeError:
            return fn(*args, **kwargs)

    return decorated
