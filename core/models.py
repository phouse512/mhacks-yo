import datetime
from flask import url_for
from core import db


class User(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    username = db.StringField(max_length=255, required=True)
    hashed_pw = db.StringField(max_length=255, required=True)
    device_token = db.StringField()

    def __unicode__(self):
        return self.username

    #meta = {
    #    'allow_inheritance': True,
    #    'indexes': ['-created_at', 'slug'],
    #    'ordering': ['-created_at']
    #}



class Comment(db.EmbeddedDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    body = db.StringField(verbose_name="Comment", required=True)
    author = db.StringField(verbose_name="Name", max_length=255, required=True)


class Status(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    user = db.ReferenceField(User)
    available = db.BooleanField(required=True)

class Group(db.Document):
    owner = db.ReferenceField(User)
    group_name = db.StringField(max_length=255, required=True)
    members = db.ListField(db.ReferenceField(User))