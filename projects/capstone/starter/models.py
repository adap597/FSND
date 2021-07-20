import os
from sqlalchemy import Column, String, Integer, create_engine, DateTime
from flask_sqlalchemy import SQLAlchemy
import json
import dateutil.parser
import sys 
from flask_migrate import Migrate


database_filename = "Casting.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "postgres://{}/{}".format('localhost:5432', database_filename)
#database_path = os.environ['DATABASE_URL']
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

class Movie(db.Model):
    __tablename__='movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    release_date = db.Column(DateTime, nullable=False)
    cast = db.relationship('Actor', backref='movie', lazy=True)

    def __repr__(self):
        return f"<Movie id = '{self.id}' title='{self.title}'>"

    def __init__ (self, title, release_date):
        self.title = title 
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return{
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
            
        }

    


class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(120), nullable=False)
    cast = db.relationship('Cast', backref='actor', lazy=True)

    def __repr__(self):
        return f"<Actor id = '{self.id}' name='{self.name}'>"

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Cast(db.Model):
    __tablename__= 'cast'

    id = db.Column(db.Integer, primary_key=True)
    actor_id=db.Column(db.Integer, db.ForeignKey('Actor.id'), nullable=False)
    movie_id=db.Column(db.Integer, db.ForeignKey('Movie.id'), nullable=False)

    def __repr__(self):
        return f'<Cast {self.id}, Actor {self.actor_id}, Movie {self.movie_id}>'


