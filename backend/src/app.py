import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Recipe, Grocery, Mesuare


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)
  app.config.from_object('config')
  db.init_app(app)
  migrate = Migrate(app,db)

  @app.after_request
  def after_reguest(response):
    response.headers.add('Access-Control-Allow-Headers', 
                          'Content-Type, Autrorizaition')
    response.headers.add('Access-Control-Allow-Methods',
      'GET, POST, PATCH, DELETE, OPTIONS')
    return response  

  # ROUTES
  '''
  endpoint GET /drinks
          contains only the drink.short() data representation
      returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
          or appropriate status code indicating reason for failure
  '''
  @app.route('/recipes')
  def get_recipes():
    try:
        recipes = Recipe.query.all()
        return jsonify({
            "success": True,
            "recipes": recipes
        }), 200
    except Exception:
        abort(422)

  # @app.route('/recipes/<int:recipe_id>')
  # @requires_auth("get:recipes-detail")
  # def get_specific_recipe():

  # @app.route('/recipes', methods=['POST'])
  # @requires_auth("post:recipes")
  # def create_recipe(token):   


  # @app.route('/recipes/<int:recipe_id>', methods=['PATCH'])
  # @requires_auth('patch:recipes')
  # def update_drinks(token, recipe_id): 


  # @app.route('/drinks/<recipe_id>', methods=['DELETE'])
  # @requires_auth('delete:recipes')
  # def delete_drinks(token, recipe_id): 



  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)