import flask
from flask import Flask

APP = Flask(__name__)
APP.config.from_object('opinator.config')


import opinator
import opinator.lib

SESSION = opinator.lib.models.create_session(APP.config['SQLALCHEMY_DATABASE_URI'])
import views
