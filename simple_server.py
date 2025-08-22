#!/usr/bin/env python3
"""
Simple Flask server for testing
"""
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config

# Create Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Override database URI for testing
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_database.db'

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Simple models for testing
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    daily_rate = db.Column(db.Float, nullable=False)
    is_available = db.Column(db.Boolean, default=True)

# Routes
@app.route('/')
def index():
    return jsonify({'message': 'Car Sharing & Detailing API', 'status': 'running'})

@app.route('/vehicles')
def get_vehicles():
    vehicles = Vehicle.query.filter_by(is_available=True).all()
    return jsonify([{
        'id': v.id,
        'make': v.make,
        'model': v.model,
        'year': v.year,
        'daily_rate': v.daily_rate
    } for v in vehicles])

@app.route('/register', methods=['POST'])
def register():
    return jsonify({'message': 'Registration endpoint'}), 201

@app.route('/login', methods=['POST'])
def login():
    return jsonify({'message': 'Login endpoint'}), 200

@app.route('/detailing/services')
def get_detailing_services():
    return jsonify([{
        'id': 1,
        'name': 'Basic Wash',
        'description': 'Exterior wash and interior vacuum',
        'base_price': 25.00
    }])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✅ Database tables created")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 