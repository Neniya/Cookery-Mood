from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#



recipe_items = db.Table('recipe_groceries', 
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id'), primary_key=True),
    db.Column('grocery_id', db.Integer, db.ForeignKey('groceries.id'), primary_key=True),
    db.Column('count', db.Float),
    db.Column('mesuare_id', db.Integer, db.ForeignKey('mesuares.id'), primary_key=True)
  )


class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    time_to_prepare = db.Column(db.String)
    cooking_time = db.Column(db.String)
    description = db.Column(db.String)
    groceries = db.relationship('Grocery', secondary = recipe_items,
                    backref = 'recipes', lazy = True)
    
class Grocery(db.Model):
    __tablename__ = 'groceries'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    mesuare =  db.relationship('Mesuare', secondary = recipe_items,
                    backref = 'groceries', lazy = True)
    

class Mesuare(db.Model):
    __tablename__ = 'mesuares' 
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    short_name = db.Column(db.String(10))