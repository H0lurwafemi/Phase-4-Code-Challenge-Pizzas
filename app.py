from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# Route to home endpoint
@app.route('/')
def home():
    return 'Welcome'

# Route to get all restaurants
@app.route('/restaurants', methods=['GET'])
def restaurants():
    # Convert list of restaurants to a dictionary
    restaurant_dict = [n.to_dict() for n in Restaurant.query.all()]
    response = make_response(jsonify(restaurant_dict), 200)
    return response

# Route to get or delete a specific restaurant by ID
@app.route('/restaurants/<int:id>', methods=['GET', 'DELETE'])
def restaurantID(id):
    # Retrieve restaurant by ID
    restaurant = Restaurant.query.filter_by(id=id).first()
    response_body = {"error": "Restaurant not found"}

    if request.method == 'GET':
        # Convert restaurant data to a dictionary
        restaurant_data = {
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address,
            'pizzas': [{'id': pizza.id, 'name': pizza.name, 'ingredients': pizza.ingredients} for pizza in
                       restaurant.pizzas]
        }

        response = make_response(jsonify(restaurant_data), 200)
        return response

    elif request.method == 'DELETE':
        # Delete associated records and the restaurant itself
        RestaurantPizza.query.filter_by(restaurant_id=id).delete()
        db.session.delete(restaurant)
        db.session.commit()
        return jsonify({}), 204

    else:
        return make_response(jsonify(response_body), 404)

# Route to get all pizzas
@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    # Convert list of pizzas to a dictionary
    pizzas_dict = [n.to_dict() for n in Pizza.query.all()]
    response = make_response(jsonify(pizzas_dict), 200)
    return response

# Route to add a pizza to a restaurant
@app.route('/restaurant_pizzas', methods=['POST'])
def post_restaurant_pizzas():
    data = request.get_json()

    price = data.get('price')
    pizza_id = data.get('pizza_id')
    restaurant_id = data.get('restaurant_id')

    # Validate price
    if price is None or not (1 <= price <= 30):
        return jsonify({"errors": ["Validation error: Price must be between 1 and 30"]}), 400

    # Check if the restaurant exists
    restaurant = Restaurant.query.get(restaurant_id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404

    # Check if the pizza exists
    pizza = Pizza.query.get(pizza_id)
    if not pizza:
        return jsonify({"error": "Pizza not found"}), 404

    # Create a new entry in the RestaurantPizza table
    restaurant_pizza = RestaurantPizza(price=price, restaurant=restaurant, pizza=pizza)
    db.session.add(restaurant_pizza)
    db.session.commit()

    # Return information about the added pizza
    return jsonify({"id": pizza.id, "name": pizza.name, "ingredients": pizza.ingredients}), 201

# Run the application
if __name__ == '__main__':
    app.run(port=5555, debug=True)
