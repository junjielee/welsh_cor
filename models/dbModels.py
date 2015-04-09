#coding: utf8

from flask.ext.mongoengine import MongoEngine

import datetime

db = MongoEngine()
t = datetime.datetime.now()
now = datetime.datetime(t.year,t.month,t.day,t.hour,t.minute,t.second)

class User(db.Document):
    name = db.StringField(max_length=30,required=True,unique=True)
    password = db.StringField(max_length=30,required=True)
    add_time = db.DateTimeField(default=now,required=True)
    last_time = db.DateTimeField(default=now,required=True)

class Task(db.Document):
    task_id = db.StringField(primary_key=True)
    name = db.StringField(max_length=50)
    detail = db.StringField(required=True)
    complete = db.IntField(default=0)
    add_time = db.DateTimeField(default=now,required=True)
    end_time = db.DateTimeField()
    user_name = db.StringField(max_length=30,required=True)
