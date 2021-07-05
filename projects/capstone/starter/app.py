from home.adap194567.FSND.projects.capstone.starter.database.models import db_drop_and_create_all
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .database.models import db_drop_and_create_all, setup_db, Actor, Movie, Cast
from auth.auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  #CORS(app)
  setup_db(app)

  db_drop_and_create_all

  CORS(app, resources={r"/*": {"origins": "*"}})

  return app

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






APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)