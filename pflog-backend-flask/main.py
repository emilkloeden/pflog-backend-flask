from werkzeug.security import generate_password_hash

from app import app, db
from models import Comment, User, Post, Role, UserRole
from routes import *


def create_tables():
    db.database.drop_tables([User, Post, Role, UserRole, Comment])
    db.database.create_tables([User, Post, Role, UserRole, Comment], safe=False)
    with db.database.atomic():
        author_role = Role(role="author")
        author_role.save()
        admin_role = Role(role="admin")
        admin_role.save()

        admin_user = User(
            username="admin",
            first_name="test",
            surname="test",
            password=generate_password_hash("test123"),
            email="admin@test.pf",
        )
        admin_user.save()

        author_user = User(
            username="author",
            first_name="test",
            surname="test",
            password=generate_password_hash("test123"),
            email="author@test.pf",
        )
        author_user.save()

        both_user = User(
            username="both",
            first_name="test",
            surname="test",
            password=generate_password_hash("test123"),
            email="both@test.pf",
        )
        both_user.save()

        UserRole.create(user=author_user, role=author_role)
        UserRole.create(user=admin_user, role=admin_role)
        # UserRole.create(user=both_user, roleboth_role)

        body1 = """Hello from <em>pflog</em>"""
        body2 = """Just an example blog."""

        posts = [
            {
                "user": author_user,
                "title": "Hello, World",
                "slug": "hello-world",
                "body": body1,
            },
            {
                "user": author_user,
                "title": "Welcome to Pflog!",
                "slug": "welcome-to-pflog",
                "body": body2,
            },
        ]
        Post.insert_many(posts).execute()


if __name__ == "__main__":
    create_tables()
    app.run(debug=True)
    # app.run()