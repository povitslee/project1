from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///warehouse.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

# Database Models
class Warehouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    aisles = db.Column(db.Integer, nullable=False)
    tiers = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'), nullable=False)
    aisle = db.Column(db.Integer, nullable=False)
    tier = db.Column(db.Integer, nullable=False)
    is_occupied = db.Column(db.Boolean, default=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    warehouse = db.relationship('Warehouse', backref='locations')
    product = db.relationship('Product', backref='locations')

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_type = db.Column(db.String(20), nullable=False)  # 'receive' or 'pick'
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    product = db.relationship('Product')
    location = db.relationship('Location')

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/warehouse', methods=['POST'])
def setup_warehouse():
    data = request.get_json()
    
    # Clear existing warehouse data
    Warehouse.query.delete()
    Location.query.delete()
    
    warehouse = Warehouse(
        name=data['name'],
        aisles=data['aisles'],
        tiers=data['tiers']
    )
    db.session.add(warehouse)
    db.session.commit()
    
    # Create locations for all aisles and tiers
    for aisle in range(1, data['aisles'] + 1):
        for tier in range(1, data['tiers'] + 1):
            location = Location(
                warehouse_id=warehouse.id,
                aisle=aisle,
                tier=tier,
                is_occupied=False
            )
            db.session.add(location)
    
    db.session.commit()
    
    return jsonify({'message': 'Warehouse setup successfully', 'warehouse_id': warehouse.id})

@app.route('/api/warehouse', methods=['GET'])
def get_warehouse():
    warehouse = Warehouse.query.first()
    if not warehouse:
        return jsonify({'error': 'No warehouse configured'}), 404
    
    return jsonify({
        'id': warehouse.id,
        'name': warehouse.name,
        'aisles': warehouse.aisles,
        'tiers': warehouse.tiers
    })

@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.get_json()
    
    # Check if SKU already exists
    existing_product = Product.query.filter_by(sku=data['sku']).first()
    if existing_product:
        return jsonify({'error': 'Product with this SKU already exists'}), 400
    
    product = Product(
        name=data['name'],
        sku=data['sku'],
        description=data.get('description', '')
    )
    db.session.add(product)
    db.session.commit()
    
    return jsonify({'message': 'Product added successfully', 'product_id': product.id})

@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'sku': p.sku,
        'description': p.description
    } for p in products])

@app.route('/api/locations', methods=['GET'])
def get_locations():
    locations = Location.query.all()
    return jsonify([{
        'id': l.id,
        'aisle': l.aisle,
        'tier': l.tier,
        'is_occupied': l.is_occupied,
        'product_name': l.product.name if l.product else None,
        'quantity': l.quantity
    } for l in locations])

@app.route('/api/receive', methods=['POST'])
def receive_item():
    data = request.get_json()
    
    # Find available location
    available_location = Location.query.filter_by(is_occupied=False).first()
    if not available_location:
        return jsonify({'error': 'No available locations in warehouse'}), 400
    
    product = Product.query.get(data['product_id'])
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    # Update location
    available_location.is_occupied = True
    available_location.product_id = product.id
    available_location.quantity = data['quantity']
    
    # Create transaction record
    transaction = Transaction(
        transaction_type='receive',
        product_id=product.id,
        location_id=available_location.id,
        quantity=data['quantity']
    )
    db.session.add(transaction)
    db.session.commit()
    
    return jsonify({
        'message': 'Item received successfully',
        'location': {
            'aisle': available_location.aisle,
            'tier': available_location.tier
        }
    })

@app.route('/api/pick', methods=['POST'])
def pick_item():
    data = request.get_json()
    
    location = Location.query.filter_by(
        aisle=data['aisle'],
        tier=data['tier']
    ).first()
    
    if not location or not location.is_occupied:
        return jsonify({'error': 'No items at this location'}), 400
    
    if location.quantity < data['quantity']:
        return jsonify({'error': 'Insufficient quantity at this location'}), 400
    
    # Update quantity
    location.quantity -= data['quantity']
    if location.quantity == 0:
        location.is_occupied = False
        location.product_id = None
    
    # Create transaction record
    transaction = Transaction(
        transaction_type='pick',
        product_id=location.product_id,
        location_id=location.id,
        quantity=data['quantity']
    )
    db.session.add(transaction)
    db.session.commit()
    
    return jsonify({'message': 'Items picked successfully'})

@app.route('/api/reports/occupancy', methods=['GET'])
def get_occupancy_report():
    warehouse = Warehouse.query.first()
    if not warehouse:
        return jsonify({'error': 'No warehouse configured'}), 404
    
    total_locations = warehouse.aisles * warehouse.tiers
    occupied_locations = Location.query.filter_by(is_occupied=True).count()
    available_locations = total_locations - occupied_locations
    
    return jsonify({
        'total_locations': total_locations,
        'occupied_locations': occupied_locations,
        'available_locations': available_locations,
        'occupancy_percentage': round((occupied_locations / total_locations) * 100, 2)
    })

@app.route('/api/reports/transactions', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.order_by(Transaction.timestamp.desc()).all()
    return jsonify([{
        'id': t.id,
        'type': t.transaction_type,
        'product_name': t.product.name,
        'location': f"Aisle {t.location.aisle}, Tier {t.location.tier}",
        'quantity': t.quantity,
        'timestamp': t.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    } for t in transactions])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000) 