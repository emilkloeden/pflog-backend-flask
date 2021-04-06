import os
from flask import Flask, session, redirect, request
from playhouse.flask_utils import FlaskDB, get_object_or_404, object_list


APP_DIR = os.path.dirname(os.path.realpath(__file__))
DATABASE = f"sqliteext:///{os.path.join(APP_DIR, 'pflog.db')}"

app = Flask(__name__)
app.config.from_object(__name__)  # TODO: configure this

db = FlaskDB(app)
