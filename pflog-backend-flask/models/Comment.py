import datetime
from peewee import *

from models.BaseModel import BaseModel
from models.User import User
from models.Post import Post


class Comment(BaseModel):
    user = ForeignKeyField(User, backref="comments")
    post = ForeignKeyField(Post, backref="comments")
    comment = TextField()
    created_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        indexes = (
            # Create a unique index on user_id, post_id and comment
            (("user", "post", "comment"), True),
        )