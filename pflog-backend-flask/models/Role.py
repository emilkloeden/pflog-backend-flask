from peewee import *

from models.BaseModel import BaseModel


class Role(BaseModel):
    role = CharField()

    def __str__(self) -> str:
        return self.role
