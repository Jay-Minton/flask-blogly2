"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    first_name = db.Column(db.Text, nullable=False)

    last_name = db.Column(db.Text, nullable=False)
    
    #make sure to fix the default image
    image_url = db.Column(db.Text, nullable =False, default="https://www.nicepng.com/png/full/888-8883726_headshot-generic-human-head-silhouette.png")

    posts = db.relationship("Post", backref="user")

class Post(db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable = False, default = datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)