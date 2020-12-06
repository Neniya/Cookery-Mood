from flask_sqlalchemy import SQLAlchemy

import os

db = SQLAlchemy()

database_name = "easylist"
DB_USERNAME = "postgres"
DB_PASSWORD = "postgres123"
database_path = database_path = os.environ['DATABASE_URL'] \
    if 'DATABASE_URL' in os.environ \
    else "postgresql://{}:{}@{}/{}".format(
        DB_USERNAME, DB_PASSWORD, 'localhost:5432', database_name)


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


'''bind recipes and items'''

class RecipeItem(db.Model):
    __tablename__ = "recipe_items"

    recipe_id = db.Column(
        db.Integer,
        db.ForeignKey("recipes.id"),
        primary_key=True,
        nullable=False)
    item_id = db.Column(
        db.Integer,
        db.ForeignKey("items.id"),
        primary_key=True,
        nullable=False)
    mesuare_id = db.Column(
        db.Integer,
        db.ForeignKey("mesuares.id"),
        primary_key=True,
        nullable=False)
    count = db.Column(db.Float, nullable=True)

    recipe = db.relationship("Recipe", backref="recipe_items")
    mesuare = db.relationship("Mesuare")
    item = db.relationship("Item", backref="recipe_items")

    def format(self):
        return {
            'recipe_id': self.recipe_id,
            'mesuare': self.mesuare.short_name,
            'item': self.item.name,
            'count': self.count
        }

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    time_to_prepare = db.Column(db.String)
    cooking_time = db.Column(db.String)
    description = db.Column(db.String)
    recipe_item = db.relationship("RecipeItem",
                                  backref="recipes", lazy=True)

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'time_to_prepare': self.time_to_prepare,
            'cooking_time': self.cooking_time,
            'description': self.description
        }

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    recipe_item = db.relationship("RecipeItem",
                                  backref="items", lazy=True)


class Mesuare(db.Model):
    __tablename__ = 'mesuares'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    short_name = db.Column(db.String(10))
