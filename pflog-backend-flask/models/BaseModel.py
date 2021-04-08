from app import db


class BaseModel(db.Model):
    class Meta:
        database = db.database