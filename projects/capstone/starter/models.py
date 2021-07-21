import os
from sqlalchemy import Column, String, Integer, create_engine, DateTime, ForeignKey
from flask_sqlalchemy import SQLAlchemy
import json
import dateutil.parser
import sys 
from flask_migrate import Migrate


database_filename = "Casting"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "postgresql:///{}".format(database_filename)
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
    actors = db.relationship('Actor', backref='movie', lazy=True)

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
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=True)

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




