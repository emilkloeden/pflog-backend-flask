import os
from flask import Flask
from playhouse.flask_utils import FlaskDB


APP_DIR = os.path.dirname(os.path.realpath(__file__))
DATABASE = f"sqliteext:///{os.path.join(APP_DIR, 'pflog.db')}"

app = Flask(__name__)
app.config.from_object(__name__)  # TODO: configure this

db = FlaskDB(app)
