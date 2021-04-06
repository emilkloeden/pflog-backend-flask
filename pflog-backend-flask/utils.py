import string


def slugify(string_: str) -> str:
    return "".join(
        [
            c
            for c in string_.lower().replace(" ", "-")
            if c in string.ascii_lowercase + string.digits + "-"
        ]
    )
