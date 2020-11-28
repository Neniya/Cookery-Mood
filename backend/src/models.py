from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#



# recipe_groceries = db.Table('recipe_groceries', 
#     db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id'), primary_key=True),
#     db.Column('grocery_id', db.Integer, db.ForeignKey('groceries.id'), primary_key=True),
#     db.Column('count', db.Float),
#     db.Column('mesuare_id', db.Integer, db.ForeignKey('mesuares.id'), primary_key=True)
#   )

class RecipeItem(db.Model):
    __tablename__ = "recipe_items"

    #id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), primary_key=True, nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), primary_key=True, nullable=False)
    mesuare_id = db.Column(db.Integer, db.ForeignKey("mesuares.id"), primary_key=True, nullable=False)
    count = db.Column(db.Float, nullable = True)
    #__table_args__ = (db.UniqueConstraint(user_id, device_id, role_id),)

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
                                backref ="recipes", lazy = True)
    def format(self):
         return {
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
                              backref ="items", lazy = True)                
    
    # def __repr__(self):
    #   return {
    #     'id': self.id,
    #     'name': self.name,
    #     'mesuare': self.mesuare
    #   }

class Mesuare(db.Model):
    __tablename__ = 'mesuares' 
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    short_name = db.Column(db.String(10))
    def __repr__(self):
      return {
        "name": self.name,
        "short_name": self.short_name
      }