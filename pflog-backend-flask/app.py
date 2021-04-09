import os
from flask import Flask
from flask_cors import CORS
from playhouse.flask_utils import FlaskDB


APP_DIR = os.path.dirname(os.path.realpath(__file__))
DATABASE = f"sqliteext:///{os.path.join(APP_DIR, 'pflog.db')}"
SECRET_KEY = 'thisistemporary'

app = Flask(__name__)
app.config.from_object(__name__)  # TODO: configure this
cors = CORS(app, resources={r"*": {"origins": "http://localhost:3000*"}})

db = FlaskDB(app)
