from flask import Flask, request, jsonify
from models.meal import Meal
from database import db
from constants import meal_not_found
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

@app.route('/meal', methods=['POST'])
def register_meal():
  data = request.json
  print(data)
  name = data.get("name")
  description = data.get("description")
  eaten_at = datetime.fromisoformat(data.get("eaten_at", datetime.utcnow())) 
  on_diet = data.get("on_diet")

  if name and description and eaten_at and on_diet:
    meal = Meal(name=name, description=description, eaten_at=eaten_at, on_diet=on_diet)
    db.session.add(meal)
    db.session.commit()
    return jsonify({"message": "Refeição cadastrada com sucesso!"}), 201
  return jsonify({"message": "Dados inválidos!"}), 400

@app.route('/meal', methods=['GET'])
def list_meals():
  meals = Meal.query.all()
  meals = [{"id": meal.id, "name": meal.name, "description": meal.description, "eaten_at": meal.eaten_at, "on_diet": meal.on_diet} for meal in meals]
  return jsonify(meals), 200

@app.route('/meal/<int:id>', methods=['GET'])
def get_meal(id):
  meal = Meal.query.get(id)
  if meal:
    return jsonify({"id": meal.id, "name": meal.name, "description": meal.description, "eaten_at": meal.eaten_at, "on_diet": meal.on_diet}), 200
  return jsonify({"message": meal_not_found}), 404

@app.route('/meal/<int:id>', methods=['PUT'])
def update_meal(id):
  data = request.json
  name = data.get("name")
  description = data.get("description")
  eaten_at = datetime.fromisoformat(data.get("eaten_at", datetime.utcnow())) 
  on_diet = data.get("on_diet")

  meal = Meal.query.get(id)
  if meal:
    meal.name = name
    meal.description = description
    meal.eaten_at = eaten_at
    meal.on_diet = on_diet
    db.session.commit()
    return jsonify({"message": "Refeição atualizada com sucesso!"}), 200
  return jsonify({"message": meal_not_found}), 404

@app.route('/meal/<int:id>', methods=['DELETE'])
def delete_meal(id):
  meal = Meal.query.get(id)
  if meal:
    db.session.delete(meal)
    db.session.commit()
    return jsonify({"message": "Refeição excluída com sucesso!"}), 200
  return jsonify({"message": meal_not_found}), 404

if __name__ == '__main__':
  app.run(debug=True) 