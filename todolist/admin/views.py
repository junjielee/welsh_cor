# -*- coding: utf-8 -*-

from flask import redirect, url_for, Blueprint
from flask.ext.admin.contrib.mongoengine import ModelView
from flask.ext import admin
from flask.ext.admin import expose

# from models import User, Task

admin_blueprint = Blueprint('admin', 'admin',
                            template_folder='templates')


class UserView(ModelView):
    list_template = 'user.html'


class TaskView(ModelView):
    admin.form_create_rules = ['_id', 'name', 'detail', 'complete',
                               'add_time', 'end_time', 'user_name']
    list_template = 'task.html'


class IndexView(admin.AdminIndexView):
    @expose('/')
    def index(self):
        return redirect(url_for('admin.user'))


# panel = admin.Admin(app, 'TodoList', index_view=IndexView())
# panel.add_view(UserView(User, name='User', endpoint='user'))
# panel.add_view(TaskView(Task, name='Task', endpoint='task'))
