from app import db
from datetime import datetime


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(120))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    ingredients = db.relationship('Ingredient', backref='recipe', lazy='dynamic')

    def __repr__(self):
        return '<Recipe {}>'.format(self.title)


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    measurement = db.Column(db.String(64))
    description = db.Column(db.String(64))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))

    def __repr__(self):
        return '<Ingredient {}>'.format(self.description)
