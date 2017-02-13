# -*- coding: utf-8 -*-

from flask import Flask
from main.views import main_blueprint
from config import Config


app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(main_blueprint, url_prefix='/todolist')


@app.route('/', endpoint='hello', methods=['GET'])
def hello():
    return "hello"


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
