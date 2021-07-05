import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import dateutil.parser
import sys 

database_path = os.environ['DATABASE_URL']

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

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

class Movie(db.model):
    __tablename__='Movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    release_date = db.Column(Integer, nullable=False)
    cast = db.relationship('Actor', backref='Movies', lazy=True)

    def __init__ (self, title, release_date, cast):
        self.title = title 
        self.release_date = release_date
        self.cast = cast

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return '<Movie {} {} {} />'.format(self.title, self.release_date, self.cast)
    


class Actor(db.model):
    __tablename__ = 'Actors'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(120), nullable=False)
    cast = db.relationship('Cast', backref='Actor', lazy=True)

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

    def __repr__(self):
        return '<Actor {} {} {} />'.format(self.name, self.age, self.gender)

class Cast(db.model):
    __tablename__= 'Cast'

    id = db.Column(db.Integer, primary_key=True)
    actor_id=db.Column(db.Integer, db.ForeignKey('Actor.id'), nullable=False)
    movie_id=db.Column(db.Integer, db.ForeignKey('Movie.id'), nullable=False)

    def __repr__(self):
        return f'<Cast {self.id}, Actor {self.actor_id}, Movie {self.movie_id}>'


