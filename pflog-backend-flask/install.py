from argparse import ArgumentParser
from getpass import getpass

from werkzeug.security import generate_password_hash

from app import db
from models import Post, Role, User, UserRole


def main():
    parser = ArgumentParser()
    parser.add_argument("--nuke", action="store_true")
    parser.add_argument("--debug", action="store_true")

    args = parser.parse_args()
    if args.nuke:
        print(f"Recreating tables...")
        drop_tables()
        unsafe_create_tables()
        insert_records(debug=args.debug)
    else:
        if not tables_already_exist():
            print(f"Creating tables...")
            create_tables()
            insert_records(debug=args.debug)
        else:
            print(
                f"Required tables already exist. Exiting. Run install.py with `--nuke` flag to drop and recreate tables."
            )


def drop_tables():
    db.database.drop_tables([User, Post, Role, UserRole])


def unsafe_create_tables():
    db.database.create_tables([User, Post, Role, UserRole], safe=False)


def tables_already_exist():
    tables = db.database.get_tables()
    return any(
        table_name in ["user", "post", "role", "userrole"] for table_name in tables
    )


def create_tables():
    db.database.create_tables([User, Post, Role, UserRole], safe=True)


def insert_dummy_posts(author):
    body1 = """Hello from <em>pflog</em>"""
    body2 = """Just an example blog."""

    posts = [
        {
            "user": author,
            "title": "Hello, World",
            "slug": "hello-world",
            "body": body1,
        },
        {
            "user": author,
            "title": "Welcome to Pflog!",
            "slug": "welcome-to-pflog",
            "body": body2,
        },
    ]
    Post.insert_many(posts).execute()


def insert_records(debug=False):
    print(f"Let's begin by creating an admin user...")
    admin_username = input("Please enter a username for the admin role: ").strip()
    admin_password = getpass("... and a password: ").strip()
    admin_first_name = input("... a given name: ").strip()
    admin_surname = input("... a surname: ").strip()
    admin_email = input("... and lastly an email address: ").strip()

    print(f"Inserting required records...")
    with db.database.atomic():
        author_role = Role(role="author")
        author_role.save()
        admin_role = Role(role="admin")
        admin_role.save()

        admin_user = User(
            username=admin_username,
            first_name=admin_first_name,
            surname=admin_surname,
            password=generate_password_hash(admin_password),
            email=admin_email,
        )
        admin_user.save()

        UserRole.create(user=admin_user, role=admin_role)
        UserRole.create(user=admin_user, role=author_role)

        if debug:
            insert_dummy_posts(admin_user)

    print(f"Done.\nRun `python3 main.py` to start the backend.")


if __name__ == "__main__":
    main()
