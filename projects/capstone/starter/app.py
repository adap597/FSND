import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
import json
from flask_cors import CORS
from .database.models import db_drop_and_create_all, setup_db, Actor, Movie, Cast
from .auth.auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  #CORS(app)
  setup_db(app)

  db_drop_and_create_all

  CORS(app, resources={r"/*": {"origins": "*"}})

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

  @app.route('/movies', methods=['GET'])
  @requires_auth("get:movies")
  def retrieve_movies(payload):
    try:
      movies = Movie.query.order_by(Movie.id).all()


      return jsonify({
        "success": True,
        "movies": movies
      }), 200
  
    except:
      if len(movies) == 0:
        abort(404)


  @app.route('/movies', methods=['POST'])
  @requires_auth("post:movie")
  def add_movie(payload):
    body = request.get_json()

    if not body:
      abort(422)

    if 'title' not in body or 'release_date' not in body or 'cast' not in body:
      abort(422)

    try:
      title = body['title']
      release_date = body['release_date']
      cast = json.dumps(body['cast'])

      movie.insert()

      return jsonify({
        'success': True,
        'movie': movie
      )}

    except:
      abort(500)
      


  return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)