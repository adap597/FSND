import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from .database.models import db_drop_and_create_all, setup_db, Actor, Movie, Cast
from config import bearer_tokens
from sqlalchemy import desc
from datetime import date

casting_assistant_auth_header = {
    'Authorization': bearer_tokens['casting_assistant']
}

casting_director_auth_header = {
    'Authorization': bearer_tokens['casting_director']
}

executive_producer_auth_header = {
    'Authorization': bearer_tokens['executive_producer']
}

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

    
    #Retrieve Movies Tests

    # Retrieve movies with authorization
    def test_retrieve_movies(self):
        res = self.client().get('/movies?page=1', headers = casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.asserTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

    #Retrieve movies with no authorization
    def test_retreive_movies_no_auth(self):
        res = self.client().get('/movies?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected')
    
    #Retrieve movies error test - no movies
    def test_retrieve_movies_404(self):
        res = self.client().get('/movies?page=5000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'No movies found')

    #Retreive Actors tests

    # Retreive actors with authorization
    def test_retrieve_actors(self):
        res = self.client().get('actors?page=1', headers = casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    # Retrieve actors without authorization
    def test_retrieve_actors_no_auth(self):
        res = self.client().get('actors?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected')

    #Retrieve actors error test - no actors in database
    def test_retreive_actors_404(self):
        res = self.client().get('actors?page=5000', headers = casting_assistant_auth_header)
        data = json.loads(res.data)
    
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'no actors found')

    #Insert actors tests

    # Insert actor with authorization
    def test_insert_actor_with_auth(self):
        json_new_actor = {
            'name': 'Idris Elba',
            'age':48,
            'gender': 'male'
        }
        
        res = self.client().post('/actors', json=json_new_actor, headers = casting_director_auth_header)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['created'], 2)
    
    def test_insert_actor_no_auth(self):
        json_new_actor = {
            'name': 'Idris Elba',
            'age': 48,
            'gender': 'male'
        }

        res = self.client().post('/actors', json=json_new_actor)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected')

    #insert actor missing data
    def test_insert_actor_missing_data(self):
        json_new_actor = {
            'name': '',
            'age': 48,
            'gender': 'male',
        }

        res = self.client().post('/actors', json=json_new_actor, headers = casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Name field missing data')

    #patch actor
    #delete actor

    #insert movie
    #patch movie
    #delete movie

        
        _
    
