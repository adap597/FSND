import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from .database.models import db_drop_and_create_all, setup_db, Actor, Movie, Cast
from config import bearer_tokens
from sqlalchemy import desc
from datetime import date

class CastingTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_test"
        self.database_path = "postgres:///{}".format(self.database_name)
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
        
    def tearDown(self):
        pass

    
    # Retrieve all movies successful test
    def test_retrieve_movies(self):
        res = self.client().get('/movies?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.asserTrue(data['success'])
    
    # Retreive all actors successful test
    def test_retrieve_actors(self):
        res = self.client().get('actors?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    # Insert actor and return list of all actors successful test
    def test_insert_actor_return_all(self):
        actor = Actor(name ='Idris Elba', age = '48', gender = 'male')
        actor.insert()
        
        res = self.client().get('/actors')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        actors = Actor.query.all()
        self.assertEqual(len(data['actors']), len(actors))
        
        _
    
