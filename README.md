# Cookery mood application 

## **Introduction**

Many people don’t want to spend time thinking about what they will eat today, tomorrow or next several days and almost nobody wants to spend a lot of time cooking something in everyday life. To simplify this process it was decided to develop an application.
 
Cookery Mood is an application where you can find easy and fast recipes.
 
The application:
 
 
1) Allows public users to view a list of recipes.
2) Allows the application users to see the recipe information.
3) Allows the application administrators to create new recipes and edit existing recipes and delete them.



## **Getting Started**

**Pre-requisites and Local Development**
Developers using this project should already have Python3, pip, and node installed on their local machines.

## DATA MODELING:
MODELS.PY

The schema for the database and helper methods to simplify API behavior are in models.py:

   * There are four tables created: Recipe, Item, Mesuare, and RecipeItem.
   * The Recipe table is used by the roles 'user' and 'administrator' to get a list of existing recipes.
   * The Item table  is used for a storage list of items, that is using for recipes.
   * The Mesuare table is used for storage list of measures, that is using for indicating couth of items in recipes.
   * The Product table has a foreign key on the User table for user_id.
   * The Recipe table, Item table, and Mesuare table have foreign keys on the RecipeItem table for recipe_id, item_id, and mesuare_id accordingly.
   * The Recipe table is used by the role 'administrator' to add new recipes.
   * The RecipeItem is used by the role 'administrator' to bind recipe's items and amount of them with recipe.
   * The Recipe table has an insert, update, delete, and format helper functions.
   * The RecipeItem has delete, and format helper functions.


### Backend

The backend contains a completed Flask server.


## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip3 install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Running the server

From within the project directory first ensure you are working using your created virtual environment.

To run the server, execute:

**On Linux :**
```bash
export FLASK_APP=api.py
export FLASK_ENV=development
flask run
```

**On Windows :**
```bash
set FLASK_APP=api.py;
set FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 



## Testing
 ### Local:
    To run the tests, run
    ```
    dropdb easylist_test
    createdb easylist_test
    psql easylist_test < easylist.psql
    python test_app.py
    ```
 ### Heroku
    Test your endpoints with [Postman](https://getpostman.com). 
    - Register 2 users - assign the User role to one and Administrator role to the other.
    - Sign into each account and make note of the tokens.
    - Import the postman collection `cookery-mood.postman_collection.json`
        --> Import -> directory/warranty-tracker-test-endpoints.postman_collection.json
    - Right-clicking the collection folder for user and administrator, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).  


## **API**
* Base URL: At present this app can be run locally (`http://127.0.0.1:5000/`) and can also be open via Heroku using the URL:
 `https://cookerymood.herokuapp.com/`
* Authentication: This application uses the Auth0 authentication method. Please see below for more details.

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:recipes-detail`
    - `post:recipes`
    - `patch:recipes`
    - `delete:recipes`
6. Create new roles for:
    - User
        - can `get:recipes-detail`
    - Administrator
        - can perform all actions 
   
## Error handling
Errors are returned as JSON objects in the following format:
`{
"success": False,
"error": 404,
"message": "resource not found"
}`

The API will return five error types when requests fail:
* 400: Best Request
* 404: Resouses not found
* 422: Not Processable
* 401: Unauthorized
* 403: Forbidden

## Endpoints

* [GET '/recipes'](#get-recipes)
* [GET '/recipes/&lt;nt:recipe_id&gt;'](#get-recipesintrecipe_id))
* [POST '/recipes'](#post-recipes)
* [PATCH '/recipes/&lt;nt:recipe_id&gt;'](#patch-recipesintrecipe_id)
* [DELETE '/recipes/&lt;nt:recipe_id&gt;'](#delete-recipesintrecipe_id)


### GET '/recipes'

* General:
    * Fetches a dictionary of recipes objects. 
    * Request Arguments: None
    * Returns: Status code 200, success value and  a list of recipes objects 

* Sample in Postman : GET `{{host}}/recipes`

```
{
    "recipes": [
        {
            "cooking_time": "10 min.",
            "description": "{1: ‘step 1’ , 2: ‘step 2'}",
            "id": 6,
            "name": "Potato salad",
            "time_to_prepare": "10 min"
        },
        {
            "cooking_time": "No cook",
            "description": "{1: ‘Blend berries, yogurt and honey or agave syrup in a food processor for 20 seconds, until it comes together to a smooth ice-cream texture. Scoop into bowls and serve.’}",
            "id": 29,
            "name": "Frozen mixed berry",
            "time_to_prepare": "2 min"
        },
        {
            "cooking_time": "5 min",
            "description": "{1: ‘Cook the gnocchi in a large pan of lightly salted, boiling water. Drain and reserve 200ml of the cooking water.’, 2: 'Heat the butter in a large frying pan. Add the gnocchi, cheese and pepper as well as 150ml of the cooking water, raise the heat a little and stir vigorously until melted and the gnocchi is well coated. Pour in more of the reserved water if you like it saucier. Season with a little salt. Transfer the gnocchi to bowls and serve with a mixed salad, if you like.'}",
            "id": 30,
            "name": "Gnocchi cacio e pepe",
            "time_to_prepare": "2 min"
        },
        {
            "cooking_time": " 1 hour(marinade)",
            "description": "{1: Toss together the cucumbers and onion in a large bowl. Combine the vinegar, water and sugar in a saucepan over medium-high heat. Bring to a boil, and pour over the cucumber and onions. Stir in dill, cover, and refrigerate until cold. This can also be eaten at room temperature, but be sure to allow the cucumbers to marinate for at least 1 hour.'}",
            "id": 32,
            "name": "Cucumber Salad",
            "time_to_prepare": "10 min"
        },
        {
            "cooking_time": "10 min.",
            "description": "{1: ‘step 1’ , 2: ‘step 2'}",
            "id": 5,
            "name": "test potato",
            "time_to_prepare": "10 min"
        },
        {
            "cooking_time": " 1 hour(marinade)",
            "description": "{1: Toss together the cucumbers and onion in a large bowl. Combine the vinegar, water and sugar in a saucepan over medium-high heat. Bring to a boil, and pour over the cucumber and onions. Stir in dill, cover, and refrigerate until cold. This can also be eaten at room temperature, but be sure to allow the cucumbers to marinate for at least 1 hour.'}",
            "id": 36,
            "name": "Cucumber Salad",
            "time_to_prepare": "10 min"
        }
    ],
    "success": true
}
```


### GET '/recipes/int:recipe_id'

* General:
    * Fetches a description of the current object.
    * Request Arguments: recipe_id
    * Returns: Status code 200, success value and a description of current recipe.

* Sample in Postman: GET `{{host}}/drecipes/30`

```
{
    "cooking_time": "5 min",
    "description": "{1: ‘Cook the gnocchi in a large pan of lightly salted, boiling water. Drain and reserve 200ml of the cooking water.’, 2: 'Heat the butter in a large frying pan. Add the gnocchi, cheese and pepper as well as 150ml of the cooking water, raise the heat a little and stir vigorously until melted and the gnocchi is well coated. Pour in more of the reserved water if you like it saucier. Season with a little salt. Transfer the gnocchi to bowls and serve with a mixed salad, if you like.'}",
    "items": [],
    "name": "Gnocchi cacio e pepe",
    "success": true,
    "time_to_prepare": "2 min"
}
```

### POST '/recipes'

* General:
    * creates a new row in the recipes table and some rows in recipe_items with recipe's items
    * requires the 'post:recipes' permission
    * Request Arguments: name(string, name of new recipe), time_to_prepare(string) cooking_time(string), description(string with dictionary{step(num): description(string)}, item_list(list of dictionaries(item id, masuare id, count))).
        Sample:
            ```
            {
                "name": "Cucumber Salad", 
                "time_to_prepare": "10 min", 
                "cooking_time": " 1 hour(marinade)", 
                "description": "{1: Toss together the cucumbers and onion in a large bowl. Combine the vinegar, water and sugar in a saucepan over medium-high heat. Bring to a boil, and pour over the cucumber and onions. Stir in dill, cover, and refrigerate until cold. This can also be eaten at room temperature, but be sure to allow the cucumbers to marinate for at least 1 hour.'}", 
                "item_list": [
                    { 
                        "count": 4, 
                        "item_id": 7,
                        "mesuare_id": 8
                    }, 
                    
                    {
                        "count": 1,  
                        "item_id": 8, 
                        "mesuare_id": 8
                    },
                    {
                        "count": 0.5,  
                        "item_id": 3, 
                        "mesuare_id": 6
                    },
                    {
                        "count": 0.75,  
                        "item_id": 9, 
                        "mesuare_id": 6
                    },
                    {
                        "count": 1,  
                        "item_id": 11, 
                        "mesuare_id": 7
                    }
                ]
            }
            ```
    * Returns: Status code 200, success value id of newly created recipe and an array containing paginated recipes.

* Sample in Postman(for role "Administrator"): POST `{{host}}/recipes`
```
{
    "created": 35,
    "recipes": [
        {
            "cooking_time": "10 min.",
            "description": "{1: ‘step 1’ , 2: ‘step 2'}",
            "id": 6,
            "name": "Potato salad",
            "time_to_prepare": "10 min"
        },
        {
            "cooking_time": "No cook",
            "description": "{1: ‘Blend berries, yogurt and honey or agave syrup in a food processor for 20 seconds, until it comes together to a smooth ice-cream texture. Scoop into bowls and serve.’}",
            "id": 29,
            "name": "Frozen mixed berry",
            "time_to_prepare": "2 min"
        },
        {
            "cooking_time": "5 min",
            "description": "{1: ‘Cook the gnocchi in a large pan of lightly salted, boiling water. Drain and reserve 200ml of the cooking water.’, 2: 'Heat the butter in a large frying pan. Add the gnocchi, cheese and pepper as well as 150ml of the cooking water, raise the heat a little and stir vigorously until melted and the gnocchi is well coated. Pour in more of the reserved water if you like it saucier. Season with a little salt. Transfer the gnocchi to bowls and serve with a mixed salad, if you like.'}",
            "id": 30,
            "name": "Gnocchi cacio e pepe",
            "time_to_prepare": "2 min"
        },
        {
            "cooking_time": " 1 hour(marinade)",
            "description": "{1: Toss together the cucumbers and onion in a large bowl. Combine the vinegar, water and sugar in a saucepan over medium-high heat. Bring to a boil, and pour over the cucumber and onions. Stir in dill, cover, and refrigerate until cold. This can also be eaten at room temperature, but be sure to allow the cucumbers to marinate for at least 1 hour.'}",
            "id": 32,
            "name": "Cucumber Salad",
            "time_to_prepare": "10 min"
        },
        {
            "cooking_time": "10 min.",
            "description": "{1: ‘step 1’ , 2: ‘step 2'}",
            "id": 5,
            "name": "test potato",
            "time_to_prepare": "10 min"
        },
        {
            "cooking_time": " 1 hour(marinade)",
            "description": "{1: Toss together the cucumbers and onion in a large bowl. Combine the vinegar, water and sugar in a saucepan over medium-high heat. Bring to a boil, and pour over the cucumber and onions. Stir in dill, cover, and refrigerate until cold. This can also be eaten at room temperature, but be sure to allow the cucumbers to marinate for at least 1 hour.'}",
            "id": 35,
            "name": "Cucumber Salad",
            "time_to_prepare": "10 min"
        }
    ],
    "success": true
}
```


### PATCH '/recipes/<int:recipe_id>'
* General:
    * Updates the recipe of the given ID if it exists.. 
    * Request Arguments: recipe_id
    * Returns: Status code 200, success value and an updated recipe's id 

* Sample in Postman(for role "Administrator"): PATCH `{{host}}/recipes/5`

```
{
    "recipe_id": 5,
    "success": true
}
```


### DELETE '/recipes/<int:recipe_id>'
* General:
    * Deletes the recipes of the given ID if it exists.. 
    * Request Arguments: recipe_id
    * Returns: Status code 200, success value, an id of the deleted record, and an array containing paginated recipes.

* Sample in Postman(for role "Administrator"): DELETE `{{host}}/recipes/35`

```
{
"deleted": "35",
    "recipes": [
        {
            "cooking_time": "10 min.",
            "description": "{1: ‘step 1’ , 2: ‘step 2'}",
            "id": 6,
            "name": "Potato salad",
            "time_to_prepare": "10 min"
        },
        {
            "cooking_time": "No cook",
            "description": "{1: ‘Blend berries, yogurt and honey or agave syrup in a food processor for 20 seconds, until it comes together to a smooth ice-cream texture. Scoop into bowls and serve.’}",
            "id": 29,
            "name": "Frozen mixed berry",
            "time_to_prepare": "2 min"
        },
        {
            "cooking_time": "5 min",
            "description": "{1: ‘Cook the gnocchi in a large pan of lightly salted, boiling water. Drain and reserve 200ml of the cooking water.’, 2: 'Heat the butter in a large frying pan. Add the gnocchi, cheese and pepper as well as 150ml of the cooking water, raise the heat a little and stir vigorously until melted and the gnocchi is well coated. Pour in more of the reserved water if you like it saucier. Season with a little salt. Transfer the gnocchi to bowls and serve with a mixed salad, if you like.'}",
            "id": 30,
            "name": "Gnocchi cacio e pepe",
            "time_to_prepare": "2 min"
        },
        {
            "cooking_time": " 1 hour(marinade)",
            "description": "{1: Toss together the cucumbers and onion in a large bowl. Combine the vinegar, water and sugar in a saucepan over medium-high heat. Bring to a boil, and pour over the cucumber and onions. Stir in dill, cover, and refrigerate until cold. This can also be eaten at room temperature, but be sure to allow the cucumbers to marinate for at least 1 hour.'}",
            "id": 32,
            "name": "Cucumber Salad",
            "time_to_prepare": "10 min"
        },
        {
            "cooking_time": "10 min.",
            "description": "{1: ‘step 1’ , 2: ‘step 2'}",
            "id": 5,
            "name": "test potato",
            "time_to_prepare": "10 min"
        }
    ],
    "success": true
}
```
## **Deployment**
The app is hosted live on heroku at the URL: 
https://cookerymood.herokuapp.com/

However, there is no frontend for this app yet, and it can only be presently used to authenticate using Auth0 by entering
credentials and retrieving a fresh token to use with curl, unit test, or postman.

## **Authors**
Kotova Evgeniia

## **Acknowledgments**
The awesome team at Udacity for the knowledge that helps me to realize this application. 


