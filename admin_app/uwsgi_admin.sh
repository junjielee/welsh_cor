#!/bin/sh


uwsgi -s 127.0.0.1:2025 --wsgi-file admin.py --processes 1 --threads 1 --disable-loggin --py-autoreload 1
