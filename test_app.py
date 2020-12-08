import os
import sys
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
# sys.path.append("../")
from api import create_app
from models import db, setup_db, Recipe, Mesuare, Item, RecipeItem

# Tokens
USER_TOKEN = os.environ['USER_TOKEN']
ADMINISTRATOR_TOKEN = os.environ['ADMINISTRATOR_TOKEN']


def init_new_recipe():
    return {
        "name": "Potato salad",
        "time_to_prepare": "10 min.",
        "cooking_time": "10 min.",
        "description": "{1: ‘step 1’ , 2: ‘step 2'}",
        "item_list": [
            {
                    "count": 2,
                    "item_id": 3,
                    "mesuare_id": 6
            },
            {
                    "count": 250,
                    "item_id": 2,
                    "mesuare_id": 2
            }
        ]
    }


class CookeryMoodTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "easylist_test"
        DB_USERNAME = "postgres"
        DB_PASSWORD = "postgres123"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            DB_USERNAME, DB_PASSWORD, 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # GET /recipes
    def test_get_paginated_recipes(self):
        res = self.client().get('/recipes')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['recipes'])

    def test_404_sent_reguesting_beyond_valid_page(self):
        res = self.client().get('/recipes?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    '''create recipe'''
    # POST /recipes
    '''Administrator'''

    def test_create_recipe(self):
        new_recipe = init_new_recipe()

        res = self.client().post(
            '/recipes',
            headers={'Authorization': 'Bearer ' + str(ADMINISTRATOR_TOKEN)},
            json=new_recipe
        )

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['recipes'])

    '''User'''

    def test_401_if_create_recipe_unauthorized(self):
        new_recipe = init_new_recipe()

        res = self.client().post(
            '/recipes',
            headers={'Authorization': 'Bearer ' + str(USER_TOKEN)},
            json=new_recipe
        )

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_422_if_recipe_creation_empty_data(self):
        new_recipe = {"name": "Potato salad",
                      "time_to_prepare": "10 min.",
                      "cooking_time": "10 min.",
                      "description": "{1: ‘step 1’ , 2: ‘step 2'}",
                      "item_list": []}
        res = self.client().post(
            '/recipes',
            headers={'Authorization': 'Bearer ' + str(ADMINISTRATOR_TOKEN)},
            json=new_recipe
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    '''Delete'''
    '''Administrator'''

    def test_delete_recipe(self):

        new_recipe = init_new_recipe()
        res_new = self.client().post(
            '/recipes',
            headers={'Authorization': 'Bearer ' + str(ADMINISTRATOR_TOKEN)},
            json=new_recipe
        )

        data_new = json.loads(res_new.data)
        id_new = data_new['created']
        res = self.client().delete(
            '/recipes/{}'.format(id_new),
            headers={'Authorization': 'Bearer ' + str(ADMINISTRATOR_TOKEN)}
        )
        data = json.loads(res.data)

        recipe = Recipe.query.filter(Recipe.id == id_new).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], str(id_new))

        self.assertTrue(len(data['recipes']))
        self.assertEqual(recipe, None)

    '''user'''

    def test_401_delete_recipe_unauthorized(self):

        res = self.client().delete(
            '/recipes/17',
            headers={'Authorization': 'Bearer ' + str(USER_TOKEN)}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # if recipe doesn't exist
    def test_404_if_recipe_does_not_exist(self):
        res = self.client().delete(
            '/recipes/10000',
            headers={'Authorization': 'Bearer ' + str(ADMINISTRATOR_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # PATCH /recipes
    '''Administrator'''

    def test_update_recipe(self):
        new_recipe = init_new_recipe()

        res = self.client().patch(
            '/recipes/5',
            headers={'Authorization': 'Bearer ' + str(ADMINISTRATOR_TOKEN)},
            json={"name": "Potato"}
        )

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['recipe_id'], "5")

    def test_404_if_updated_recipe_does_not_exist(self):
        res = self.client().patch(
            '/recipes/10000',
            headers={'Authorization': 'Bearer ' + str(ADMINISTRATOR_TOKEN)},
            json={"name": "Potato"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


if __name__ == "__main__":
    unittest.main()
