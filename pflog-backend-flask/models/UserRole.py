from peewee import *

from models.BaseModel import BaseModel
from models.User import User
from models.Role import Role


class UserRole(BaseModel):
    user = ForeignKeyField(User, backref="user_roles")
    role = ForeignKeyField(Role, backref="user_roles")

    class Meta:
        indexes = (
            # Create a unique index on user_id and role_id
            (("user", "role"), True),
        )
