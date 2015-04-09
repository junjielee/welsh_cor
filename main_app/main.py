#coding: utf8

from flask import Flask, request, url_for, redirect, render_template, g, session, flash

import pymongo
import datetime
import sys

dbconn = pymongo.MongoClient().todo
dbconn.task.ensure_index([('_id', 1)])

application = Flask(__name__)
#app.secret_key = 'todolist2015'

#insert config file
sys.path.insert(0, '/root/todo-list')
from config import Config

application.config.from_object(Config)


@application.route('/todolist',methods=['GET','POST'])
def index():
    user_name = session.get('username','')
    if user_name == '':
        return redirect('/todolist/login')
    t = datetime.datetime.now()
    now = datetime.datetime(t.year,t.month,t.day,t.hour,t.minute,t.second)
    err_msg = ''

    if request.method == 'POST':
        _id = user_name + now.strftime('%Y%m%e%H%M%S')
        task_name = ''
        detail = request.form.get('task_detail')
        complete = 0
        add_time = now
        task = dbconn.task.find_one({'_id':_id})
        if task == None:
            dbconn.task.insert({'_id':_id, 'name':task_name,
                'detail':detail,'complete': complete, 
                'add_time': add_time,'user_name':user_name})
        else:
            err_msg = '任务id有相同'
        return redirect('/todolist')

    begin = datetime.datetime.combine(datetime.date.today(),
        datetime.time.min)
    end = datetime.datetime.combine(datetime.date.today(),
        datetime.time.max)

    list_task = dbconn.task.find({'$or':[{'user_name':user_name,
        'add_time': {'$gte':begin, '$lte':end}},{'user_name':user_name,
        'add_time': {'$lt':begin},'complete':0}]}).sort(
        'add_time',pymongo.DESCENDING).sort(
        'complete',pymongo.ASCENDING)

    #print list_task.count()
    g.list_task = list_task
    g.err_msg = err_msg
    g.str_date = now.strftime('%Y-%m-%d')
    return render_template('main.html')

@application.route('/todolist/login',methods=['GET','POST'])
def login():
    status = {'ret':1,'event':'success'}
    if request.method == 'POST':
        t = datetime.datetime.now()
        now = datetime.datetime(t.year,t.month,t.day,t.hour,t.minute,t.second)
        name = request.form.get('name')
        password = request.form.get('password')
        user = dbconn.user.find_one({'name':name})
        #print user
        if user == None:
            #sign up
            dbconn.user.insert({'name':name,'password':password})
            session['username'] = name
            return redirect('/todolist')
        else:    
            #login 还没添加密码判断是否正确
            if user['password'] == password:
                dbconn.user.update({'name':name},{'$set':{'last_time':now}})
                session['username'] = user['name']
                return redirect('/todolist')
            else:
                status['ret'] = 0
                status['event'] = 'fail to login because the password error'

    return render_template('login.html',status=status)

@application.route('/todolist/complete/<_id>')
def complete(_id):
    t = datetime.datetime.now()
    now = datetime.datetime(t.year,t.month,t.day,t.hour,t.minute,t.second)
    task = dbconn.task.find_one({'_id':_id})
    complete = 1
#    if task[u'complete'] == 1:
#        complete = 1
    dbconn.task.update({'_id':_id}, {'$set':{'complete':complete,'end_time':now}})
    
    return redirect('/todolist')

if __name__ == '__main__':
    application.debug = True
    application.run(host='0.0.0.0',port=2026)

