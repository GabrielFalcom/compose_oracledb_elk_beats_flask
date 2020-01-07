import cx_Oracle
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle://system:oracle@db:1521/xe'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle://system:oracle@localhost:1521/xe'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app, resources={r'/*': {'origins': '*'}})

db = SQLAlchemy(app)

from app import routes
from app import  api
