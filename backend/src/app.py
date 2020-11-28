import os
import sys
import json
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Recipe, Mesuare, Item, RecipeItem
from .auth.auth import AuthError, requires_auth

# paginate recipes (RECIPES_PER_PAGE - recipes per page)
RECIPES_PER_PAGE = 10



def paginate_recipes(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * RECIPES_PER_PAGE
    end = start + RECIPES_PER_PAGE
    formatted_recipes = [recipe.format() for recipe in selection]
    return formatted_recipes[start:end]

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
  endpoint GET /recipes
          contains recipes names
      returns status code 200 and json {"success": True, "recipes": recipes} where drinks is the list of drinks
          or appropriate status code indicating reason for failure
  '''
  @app.route('/recipes')
  def get_recipes():
    try:
        
        selection = Recipe.query.all()
        current_recipes = paginate_recipes(request, selection)
        # error 404. if there isn't any recipes on the page
        if len(current_recipes) == 0:
            abort(404)
        
        return jsonify({
            "success": True,
            "recipes": current_recipes
        }), 200
    except Exception:
        abort(422)


       

       

  '''
  endpoint GET /recipes/<int:recipe_id>
          requires the 'get:recipes-detail' permission
      returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of ingredients
          or appropriate status code indicating reason for failure
  '''
  @app.route('/recipes/<int:recipe_id>')
  @requires_auth("get:recipes-detail")
  def get_specific_recipe(token, recipe_id):
    try:
        recipe = Recipe.query.get(recipe_id)
        name = recipe.name
        item_list = []
        
        items = db.session.query(RecipeItem)\
          .join(Item)\
          .join(Mesuare)\
          .filter(
            RecipeItem.recipe_id == 1, 
            RecipeItem.item_id == Item.id,
            RecipeItem.mesuare_id == Mesuare.id
            )\
          .all()
        for recipe_item in items:
          item_list.append(
            {
            'item': recipe_item.item.name,
            'mesuare': recipe_item.mesuare.short_name,
            'count': recipe_item.count
            }
          )
           
        return jsonify({
            "success": True,
            "name": recipe.name,
            "time_to_prepare": recipe.time_to_prepare,
            "cooking_time": recipe.cooking_time,
            "description": recipe.description,
            "items": item_list 
        }), 200

    except Exception:
        abort(422)

  @app.route('/recipes', methods=['POST'])
  @requires_auth("post:recipes")
  def create_recipe(token):   
    try:
        if request.data:
            print("1")
            body = request.get_json()
            new_name = body.get('name')
            print(new_name)
            new_time_to_prepare = body.get('time_to_prepare')
            print(new_time_to_prepare)
            new_cooking_time = body.get('cooking_time')
            print(new_cooking_time)
            new_description = body.get('description')
            print(new_description)
            new_item_list = body.get('item_list')
            print(new_item_list)
            new_recipe = Recipe(
              name = new_name,
              time_to_prepare = new_time_to_prepare,
              cooking_time = new_cooking_time,
              description = new_description,
              )
    
            db.session.add(new_recipe)
            db.session.commit()
            
            for item in new_item_list:
              print(item)
              new_recipeItem = RecipeItem(
                recipe_id = new_recipe.id,
                item_id = item["item_id"],
                mesuare_id = item["mesuare_id"],
                count = item["count"]
                )
              #RecipeItem.insert(new_recipeItem) 
              db.session.add(new_recipeItem)
              
            db.session.commit()

            '''Pagination'''
            selection = Recipe.query.all()
            current_recipes = paginate_recipes(request, selection)
            '''error 404. if there isn't any recipes on the page'''
            if len(current_recipes) == 0:
                abort(404)
        
            
            return jsonify({
                "success": True,
                "recipes": current_recipes
            }), 200
           
    except Exception:
        db.session.rollback()
        print(sys.exc_info())
        abort(422)
    finally:
        db.session.close()    

  @app.route('/recipes/<int:recipe_id>', methods=['PATCH'])
  @requires_auth('patch:recipes')
  def update_recipe(token, recipe_id): 
    '''Updates drink by id'''
    try:
        recipe = Recipe.query.filter(Recipe.id == recipe_id).one_or_none()
        print(recipe_id)
        ''' responds with a 404 error if <id> is not found'''
        if recipe is None:
            abort(404)

        ''' update the corresponding row for <id>'''
        body = request.get_json()
        recipe.name = body.get('name')
        recipe.update()

        return jsonify({
            'success': True,
            'recipes': recipe.name
        }), 200
    except Exception:
        abort(422)


  @app.route('/recipes/<recipe_id>', methods=['DELETE'])
  @requires_auth('delete:recipes')
  def delete_recipe(token, recipe_id): 
    '''Delete recipe by id'''
    try:
        recipe = Recipe.query.filter(Recipe.id == recipe_id).one_or_none()
        '''responds with a 404 error if <id> is not found'''
        print(recipe_id)
        if recipe is None:
            abort(404)

        '''delete all items associate with deleted recipe'''
        recipe_items = RecipeItem.query.filter(
                        RecipeItem.recipe_id == recipe_id).all()
        for item in recipe_items:
          item.delete()

        ''' deletes the corresponding row for <id>'''  
        recipe.delete()
    
        return jsonify({
            'success': True,
            'delete': recipe_id
        })
    except Exception:
        abort(422)

  # Error Handling
  '''
  error handling for unprocessable entity
  '''


  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "unprocessable"
      }), 422


  '''
  error handling for 404 resource not found
  '''
  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": "resource not found"
      }), 404


  '''
  error handling for 401 Unauthorized
  '''
  @app.errorhandler(401)
  def not_unauthorized(error):
      return jsonify({
          "success": False,
          "error": 401,
          "message": "Unauthorized"
      }), 401


  '''
  error handler for AuthError
  '''
  @app.errorhandler(AuthError)
  def handle_auth_error(ex):
      """
      Receive the raised authorization error and propagates it as response
      """
      response = jsonify(ex.error)
      response.status_code = ex.status_code
      return response
  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)