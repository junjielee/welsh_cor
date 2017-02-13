# -*- coding: utf-8 -*-

import datetime

from flask import flash, request, redirect, render_template, g, session, url_for
from flask import Blueprint
from mongoengine.queryset.visitor import Q

from models import User, Task


main_blueprint = Blueprint('todolist', __name__,
                           template_folder='templates', static_folder='static')


@main_blueprint.route('/', endpoint='index', methods=['GET', 'POST'])
def index():
    username = session.get('username', '')
    if username == '':
        return redirect(url_for('todolist.login'))

    now = datetime.datetime.now().replace(microsecond=0)
    err_msg = ''

    if request.method == 'POST':
        task_id = username + now.strftime('%Y%m%e%H%M%S')
        detail = request.form.get('task_detail', '')

        try:
            Task.objects.get({'task_id': task_id})
        except Task.DoesNotExist:
            Task(task_id=task_id,
                 detail=detail,
                 add_time=now,
                 username=username).save()
        else:
            flash(u'任务id有相同')
        return redirect(url_for('todolist.index'))

    begin = datetime.datetime.combine(datetime.date.today(),
                                      datetime.time.min)
    end = datetime.datetime.combine(datetime.date.today(),
                                    datetime.time.max)

    list_task = Task.objects(
        Q(username=username, add_time__gte=begin, add_time__lte=end) |
        Q(username=username, add_time__lt=begin, complete=0)
    ).order_by('-add_time', 'complete')
    # list_task = Task.objects({
    #     '$or': [{
    #         'user_name': user_name,
    #         'add_time': {'$gte': begin, '$lte': end}},
    #         {'user_name': user_name,
    #          'add_time': {'$lt': begin},
    #          'complete': 0
    #     }]}).sort(
    #         'add_time', pymongo.DESCENDING).sort(
    #         'complete', pymongo.ASCENDING)

    g.list_task = list_task
    g.err_msg = err_msg
    g.str_date = now.strftime('%Y-%m-%d')
    return render_template('main.html')


@main_blueprint.route('/login', endpoint='login', methods=['GET', 'POST'])
def login():
    status = {'ret': 1, 'event': 'success'}
    if request.method == 'POST':
        t = datetime.datetime.now()
        now = datetime.datetime(t.year, t.month, t.day, t.hour, t.minute, t.second)
        name = request.form.get('name')
        password = request.form.get('password')
        try:
            user = User.objects.get(name=name)
        except User.DoesNotExist:
            User(name=name, password=password).save()
            session['username'] = name
            return redirect(url_for('todolist.index'))
        else:
            # login 还没添加密码判断是否正确
            if user['password'] == password:
                # dbconn.user.update({'name': name}, {'$set': {'last_time': now}})
                user['last_time'] = now
                user.save()
                session['username'] = user['name']
                return redirect(url_for('todolist.index'))
            else:
                status['ret'] = 0
                status['event'] = 'fail to login because the password error'

    return render_template('login.html', status=status)


@main_blueprint.route('/complete/<_id>', endpoint='complete')
def complete(_id):
    now = datetime.datetime.now().replace(microsecond=0)
    Task.objects(task_id=_id).update_one(complete=1, end_time=now)

    return redirect(url_for('todolist.index'))
