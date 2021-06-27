from flask import Flask
from flask.templating import render_template
from config import Config
from .api.routes import api
from .site.routes import site
from .authentication.routes import auth
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from marvel_heroes.models import db as root_db, login_manager, ma
from flask_cors import CORS
from flask.json import JSONEncoder
from marvel_heroes.helpers import JSONEncoder

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(api)
app.register_blueprint(site)
app.register_blueprint(auth)

root_db.init_app(app)
migrate = Migrate(app, root_db)
login_manager.init_app(app)
ma.init_app(app)

app.json_encoder = JSONEncoder

CORS(app)
