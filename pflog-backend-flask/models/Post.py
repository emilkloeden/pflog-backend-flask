import datetime
from peewee import *

from models.BaseModel import BaseModel
from models.User import User


class Post(BaseModel):
    user = ForeignKeyField(User, backref="posts")
    post_id = AutoField()
    title = CharField()
    slug = CharField()
    body = TextField()
    created_date = DateTimeField(default=datetime.datetime.now)
    published_date = DateTimeField(default=datetime.datetime.now)
    is_published = BooleanField(default=True)