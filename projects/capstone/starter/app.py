import os
import unittest
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
import json
from flask_cors import CORS
from models import setup_db, Actor, Movie
from auth.auth import requires_auth, AuthError

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  #CORS(app)
  setup_db(app)

  CORS(app)

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')

    return response

  @app.route('/')
  def health():
    return jsonify({
      'health': 'healthy'
    }), 200


   # Get list of actors 

  @app.route('/actors', methods=['GET'])
  @requires_auth('get:actors')
  def retrieve_actors():
    actors = Actor.query.all()

    if not actors:
      abort(404)

    return jsonify({
      'success' : True,
      'actors': [actor.format() for actor in actors]
    }), 200

  # Get list of movies

  @app.route('/movies', methods=['GET'])
  @requires_auth('get:movies')
  def retrieve_movies():
    movies = Movie.query.all()

    if not movies:
      abort(404)
    
    return jsonify({
      'success': True,
      'movies': [movie.format() for movie in movies]
    }), 200

  # Add a new actor

  @app.route('/actors', methods=['GET','POST'])
  @requires_auth('post:actors')
  def add_actor(payload):
    body = request.get_json()

    if not body:
      abort(422)
    if 'name' not in body or 'age' not in body or 'gender' not in body:
      abort(422)
    
    try:
      name = body['name']
      age = body['age']
      gender = body['gender']
      actor = Actor(name=name, age=age, gender=gender)

      actor.insert()

      return jsonify({
        'success': True,
        'actors': actor.format()
      })
    except:
      abort(500)


  # Update actor
    
  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def update_actor(payload, id):
    body = request.get_json
    actor = Actor.query.get(id)

    if actor is None:
      abort(404)
    
    try:
      if 'name' in body:
        actor.name = body['name']
      if 'age' in body:
        actor.age = body['age']
      if 'gender' in body:
        actor.gender = body['gender']
      
      actor.update()

      return jsonify({
        'success': True,
        'actor': actor.format()
      })
      
    except:
      abort(404)

  # Delete Actor
  
  @app.route('/actors/<int:id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(payload, id):
    
    actor = Actor.query.filter(Actor.id == id).one_or_none()

    if actor is None:
      abort(404)

    actor.delete()

    return jsonify({
      'success': True,
      'delete': actor.id
    })


  # Add movie

  @app.route('/movies', methods=['POST'])
  @requires_auth("post:movies")
  def add_movie(payload):
    body = request.get_json()

    if not body:
      abort(422)

    if 'title' not in body or 'release_date' not in body:
      abort(422)

    try:
      title = body['title']
      release_date = body['release_date']
      movie = Movie(title=title, release_date=release_date)

      movie.insert()

      return jsonify({
        'success': True,
        'movie': movie.format()
      })

    except:
      abort(500)
      
  # Update movie

  @app.route('/movies/<int:id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def update_movie(payload, id):
    body = request.get_json()
    movie = Movie.query.get(id)

    if movie is None:
      abort(404)
    
    try:
      if 'title' in body:
        movie.title = body['title']
      if 'release_date' in body:
        movie.release_date = body['release_date']
      
      movie.update()

      return jsonify({
        'success': True,
        'movie': movie.format()
      })
    
    except:
      abort(404)
    
  # Delete movie

  @app.route('/movies/<int:id>', methods= ['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(payload, id):

    movie = Movie.query.filter(Movie.id == id).one_or_none()

    if movie is None:
      abort(404)
    
    movie.delete()

    return jsonify({
      'success': True,
      'delete': movie.id
    })

# Malformed request error - the request cannot be processed due to client error
  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          'success': False,
          'error': 400,
          'message': 'bad request'
          }), 400

# No authorization error - authentication has not been provided


  @app.errorhandler(AuthError)
  def unauthorized(error):
      return jsonify({
          'success': False,
          'error': 401,
          'message': 'unauthorized'
          }), 401

# No permission error
# Used to handle requests where permission missing for user


  @app.errorhandler(403)
  def forbidden(error):
      return jsonify({
          'success': False,
          'error': 403,
          'message': 'forbidden'
          }), 403

# Resource not found error


  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          'success': False,
          'error': 404,
          'message': 'resource not found'
          }), 404

# Unprocessable error


  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          'success': False,
          'error': 422,
          'message': 'unprocessable'
          }), 422


# Internal server error


  @app.errorhandler(500)
  def internal_server_error(error):
      print (error)
      return jsonify({
          'success': False,
          'error': 500,
          'message': 'internal server error'
          }), 500


  @app.errorhandler(AuthError)
  def handleAuthError(_ErR_):
      response = jsonify(_ErR_.error)
      response.status_code = _ErR_.status_code
      return response

  return app


app = create_app()

#if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=8080, debug=True)