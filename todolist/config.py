# -*- coding: utf-8 -*-


class Config(object):
    """gloabal config file"""
    MONGODB_SETTINGS = {
        'host': 'localhost',
        'port': 27017,
        'db': 'todo'
    }
    SECRET_KEY = 'todolist2015'
