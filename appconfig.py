#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask
from flask_moment import Moment
from flask_wtf import CsrfProtect

csrf = CsrfProtect()

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)
csrf.init_app(app)