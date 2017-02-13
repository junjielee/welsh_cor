# -*- coding: utf-8 -*-

from flask import Flask
from main.views import main_blueprint
from config import Config


app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(main_blueprint)


if __name__ == "__main__":
    app.DEBUG = True
    app.run(host='0.0.0.0', port=5000)
