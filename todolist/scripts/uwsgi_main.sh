#!/bin/sh

#uwsgi --socket=/tmp/todo_list_main.socket --chmod-socket=666 -w main_app/main:app --processes 2 --threads 1 --disable-logging --stats 127.0.0.1:9528

uwsgi -s 127.0.0.1:2026 --wsgi-file main.py --processes 2 --threads 1 --disable-loggin
