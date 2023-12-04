from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

# Create an instance of SQLAlchemy
db = SQLAlchemy()

# Define the Restaurant model
class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'
    serialize_rules = ('restaurant_pizzas.restaurant')

    # Define columns for the restaurants table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    address = db.Column(db.String)
    
    # Establish a relationship with the RestaurantPizza model using backref
    pizzas = db.relationship('RestaurantPizza', backref='restaurant')

# Define the Pizza model
class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'
    serialize_rules = ('restaurant_pizzas.pizza')

    # Define columns for the pizzas table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    ingredients = db.Column(db.String)
    
    # Establish a relationship with the RestaurantPizza model using backref
    restaurants = db.relationship('RestaurantPizza', backref='pizza')

# Define the RestaurantPizza model
class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'
    serialize_rules = ('-restaurant.restaurant_pizzas', '-pizza.restaurant_pizzas')

    # Define columns for the restaurant_pizzas table
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
