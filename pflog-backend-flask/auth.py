from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
from app import app, db
from models import User

# auth = HTTPBasicAuth(app, db, user_model=User)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    user = User.select().where(User.username == username).first()
    if not user:
        return False
    if username == user.username and check_password_hash(user.password, password):
        return user
    return False


@auth.get_user_roles
def get_user_roles(user):
    return [user_role.role.role for user_role in user.user_roles]