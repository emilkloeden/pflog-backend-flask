import datetime
from peewee import *

from models.BaseModel import BaseModel


class User(BaseModel):
    username = CharField(unique=True)
    first_name = CharField()
    surname = CharField()
    password = CharField()  # TODO: confirm this
    email = CharField(unique=True)
    join_date = DateTimeField(default=datetime.datetime.now)

    def __str__(self) -> str:
        return self.username