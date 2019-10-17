from app import app, db
from app.models import Recipe, Ingredient
from flask import request, jsonify
from sqlalchemy import exc


@app.route('/create', methods=['POST'])
def create_dinspiration():
    if request.json['title'] is None:
        return jsonify({'error': 'Title cannot be blank!'})

    recipe = Recipe()
    recipe.title = request.json['title']
    if request.json['description'] is not None:
        recipe.description = request.json['description']

    try:
        db.session.add(recipe)
        db.session.commit()
    except exc.SQLAlchemyError:
        return jsonify({'error': 'Some Error has occurred!!!'})

    if request.json['ingredients'] is not None:
        ingredients = request.json['ingredients']
        for ingredient in ingredients:
            i = Ingredient(
                quantity=ingredient['quantity'],
                measurement=ingredient['measurement'],
                description=ingredient['description'],
                recipe=recipe
            )
            try:
                db.session.add(i)
                db.session.commit()
            except exc.SQLAlchemyError:
                return jsonify({'error': 'Some Error has occurred adding an ingredient!!!'})

    new_recipe = serialized_recipe(recipe)
    return jsonify(new_recipe)


@app.route('/', methods=['GET'])
def get_dinspirations():
    recipe_objects = Recipe.query.all()
    recipes = []
    for recipe_ojb in recipe_objects:
        recipes.append(serialized_recipe(recipe_ojb))

    return jsonify(recipes)


def serialized_recipe(recipe):
    ingredients = recipe.ingredients.all()
    ingredients_array = []

    for ingredient in ingredients:
        ingredients_array.append({
            'id': ingredient.id,
            'quantity': ingredient.quantity,
            'measurement': ingredient.measurement,
            'description': ingredient.description,
            'recipe_id': ingredient.recipe_id
        })

    return {
        'id': recipe.id,
        'title': recipe.title,
        'description': recipe.description,
        'timestamp': recipe.timestamp,
        'ingredients': ingredients_array
    }
