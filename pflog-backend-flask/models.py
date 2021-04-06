import datetime

from peewee import *
from app import db


class BaseModel(db.Model):
    class Meta:
        database = db.database


class User(BaseModel):
    first_name = CharField()
    surname = CharField()
    password = CharField()  # TODO: confirm this
    email = CharField(unique=True)
    join_date = DateTimeField(default=datetime.datetime.now)

    def __str__(self) -> str:
        return self.first_name


class Post(BaseModel):
    user = ForeignKeyField(User, backref="posts")
    post_id = AutoField()
    title = CharField()
    slug = CharField()
    body = TextField()
    created_date = DateTimeField(default=datetime.datetime.now)
    published_date = DateTimeField(default=datetime.datetime.now)
    is_published = BooleanField(default=True)