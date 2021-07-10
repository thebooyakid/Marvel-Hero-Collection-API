from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from flask_login import UserMixin, LoginManager
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150), nullable = True, default='')
    username = db.Column(db.String(80), unique = True, nullable = False)
    email = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String, nullable = True, default='')
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    token = db.Column(db.String, default = '', unique = True)   

    def __init__(self,email,username = '',name = '', id = '', password = ''):
        self.id = self.set_id()
        self.name = name
        self.username = username
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(24)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
    def set_token(self, length):
        return secrets.token_hex(length)

    def __repr__(self):
        return f"You're in, {self.name}"

class Hero(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(500))
    comics_appeared_in = db.Column(db.Integer)
    super_power = db.Column(db.String(500))
    # date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_token = db.Column(db.String(100),db.ForeignKey('user.token'), nullable = False)

    def __init__(self,name,description,comics_appeared_in,super_power,user_token,id =''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.comics_appeared_in = comics_appeared_in
        self.super_power = super_power
        # self.date_created = date_created
        # self.owner = owner
        self.user_token = user_token

    def set_id(self):
        return(secrets.token_urlsafe())

    def __repr__(self):
        return f"{self.name} has been added"

class HeroSchema(ma.Schema):
    class Meta:
        fields = ['id','name','description','comics_appeared_in','super_power','date_created','owner']

hero_schema = HeroSchema()
heroes_schema = HeroSchema(many=True)
