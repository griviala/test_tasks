from peewee import *
import datetime
from db import db


class BaseModel(Model):
    class Meta:
        database = db


class Task(BaseModel):
    title = CharField(max_length=150)
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
