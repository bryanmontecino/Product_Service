"""
Author: Bryan Montecino
File: product.py
Date: September 24, 2023
Assignment: REST APIs
Objective: 
The objective of this assignment is to create a microservices application for grocery shopping.
Developed two Flask microservices, ”Product Service” and ”Cart Service,” with specific endpoints.
Deployed both services on the Render platform. 
Benefits:
This assignment helped me gain practical experience in microservices architecture, API development with Flask, and cloud deployment
"""


from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuration for SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kachowproducts.db'
db = SQLAlchemy(app)

# Define a Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# Endpoint to retrive available products from Product Service
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_list = []
    for product in products:
        product_list.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'quantity': product.quantity
        })
    return jsonify(product_list)

# Endpoint to pull a unique product from the database
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if product:
        product_data = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'quantity': product.quantity
        }
        return jsonify(product_data)
    return jsonify({'message': 'Product not found'}), 404

# Endpoint to add a product, utilizing the product's name, price and quantity
@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    new_product = Product(
        name=data['name'],
        price=data['price'],
        quantity=data['quantity']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({
        'id': new_product.id,
        'name': new_product.name,
        'price': new_product.price,
        'quantity': new_product.quantity
    }), 201

if __name__ == '__main__':
    # db.create_all()
    app.run(host='0.0.0.0', port=80)  # Use host '0.0.0.0' and port 80 for Render
