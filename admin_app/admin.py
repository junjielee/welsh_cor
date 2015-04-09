#coding: utf8

from flask import Flask, redirect
from flask.ext.mongoengine import MongoEngine
from flask.ext.admin.contrib.mongoengine import ModelView
from flask.ext import admin
from flask.ext.admin import form, expose

import sys

application = Flask(__name__)

#insert config file
sys.path.insert(0, '/root/todo-list')
from config import Config
application.config.from_object(Config)

#insert models
sys.path.insert(0, '/root/todo-list/models')
import dbModels

db = MongoEngine()
db.init_app(application)

class UserView(ModelView):
    list_template = 'user.html'

class TaskView(ModelView):
    admin.form_create_rules = ['_id','name','detail','complete',
        'add_time','end_time','user_name']
    list_template = 'task.html'

class IndexView(admin.AdminIndexView):
    @expose('/')
    def index(self):
        return redirect('admin/user')

panel = admin.Admin(application, 'TodoList', index_view=IndexView())
panel.add_view(UserView(dbModels.User,name='User',endpoint='user'))
panel.add_view(TaskView(dbModels.Task,name='Task',endpoint='task'))

if __name__ == '__main__':
    application.debug = True
    application.run(host='0.0.0.0', port=2025)
