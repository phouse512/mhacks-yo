import datetime
from flask import url_for
from core import db


class User(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    first_name = db.StringField(max_length=255, required=True)
    last_name = db.StringField(max_length=255, required=True)
    hashed_pw = db.StringField(max_length=255, required=True)
    device_token = db.StringField()
    phone = db.StringField(max_length=255, required=True)
    friends = db.ListField(db.ReferenceField('self'))

    def __unicode__(self):
        return "%s %s" % (self.first_name,self.last_name)

    #meta = {
    #    'allow_inheritance': True,
    #    'indexes': ['-created_at', 'slug'],
    #    'ordering': ['-created_at']
    #}



class FriendRequest(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    requester = db.ReferenceField(User)
    requestee = db.ReferenceField(User)
    status = db.BooleanField(required=True, default=False)

class Group(db.Document):
    owner = db.ReferenceField(User)
    group_name = db.StringField(max_length=255, required=True)
    members = db.ListField(db.ReferenceField(User))

class Status(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    user = db.ReferenceField(User)
    group = db.ReferenceField(Group)
    available = db.BooleanField(required=True)