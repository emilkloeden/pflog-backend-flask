from app import app, db
from models import User, Post
from routes import *


def create_tables():
    db.database.drop_tables([User, Post])
    db.database.create_tables([User, Post], safe=False)
    with db.database.atomic():
        user = User(
            first_name="test", surname="test", password="test123", email="test@test.pf"
        )
        user.save()

        body1 = """Hello from <em>pflog</em>"""
        body2 = """Just an example blog."""

        posts = [
            {
                "user": user,
                "title": "Hello, World",
                "slug": "hello-world",
                "body": body1,
            },
            {
                "user": user,
                "title": "Welcome to Pflog!",
                "slug": "welcome-to-pflog",
                "body": body2,
            },
        ]
        Post.insert_many(posts).execute()


if __name__ == "__main__":
    create_tables()
    # app.run(debug=True)
    app.run()