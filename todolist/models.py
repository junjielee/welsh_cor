# -*- coding: utf-8 -*-

import datetime
# from flask.ext.mongoengine import MongoEngine
import mongoengine

# from .run import app

# db = MongoEngine()
now = datetime.datetime.now().replace(microsecond=0)
mongoengine.connect('todo', host='127.0.0.1', port=27017)


class User(mongoengine.Document):
    """用户表"""

    name = mongoengine.StringField(max_length=30, required=True, unique=True)
    password = mongoengine.StringField(max_length=30, required=True)
    add_time = mongoengine.DateTimeField(default=now, required=True)
    last_time = mongoengine.DateTimeField(default=now, required=True)


class Task(mongoengine.Document):
    """任务表"""

    task_id = mongoengine.StringField(primary_key=True)
    name = mongoengine.StringField(max_length=50, default="")
    detail = mongoengine.StringField(required=True)
    complete = mongoengine.IntField(default=0)
    add_time = mongoengine.DateTimeField(default=now, required=True)
    end_time = mongoengine.DateTimeField()
    username = mongoengine.StringField(max_length=30, required=True)
