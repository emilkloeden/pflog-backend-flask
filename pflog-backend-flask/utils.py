import string
from flask import request

from werkzeug.security import check_password_hash
from base64 import b64decode

from models import User


def slugify(string_: str) -> str:
    return "".join(
        [
            c
            for c in string_.lower().replace(" ", "-")
            if c in string.ascii_lowercase + string.digits + "-"
        ]
    )
