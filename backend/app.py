"""
Flask API Application for Pharmacy Management System
RESTful API endpoints for all pharmacy operations
"""

from flask import Flask, request, jsonify
from flask.json.provider import JSONProvider
from flask_cors import CORS
from datetime import datetime
import os
import json
from bson import ObjectId
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Custom JSON provider to handle ObjectId serialization
class CustomJSONProvider(JSONProvider):
    def dumps(self, obj, **kwargs):
        return json.dumps(obj, default=str, **kwargs)
    
    def loads(self, s):
        return json.loads(s)

# Import database configuration and repositories
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database.config import db_config
from backend.database.operations import (
    medication_repo, customer_repo, prescription_repo, 
    sale_repo, user_repo
)

def create_app():
    """Create and configure Flask app"""
    app = Flask(__name__)
    
    # Set custom JSON provider for ObjectId serialization
    app.json = CustomJSONProvider(app)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')
    app.config['DEBUG'] = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Enable CORS for frontend integration
    CORS(app)
    
    # Connect to MongoDB
    if not db_config.connect_to_mongodb():
        raise Exception("Failed to connect to MongoDB")
    
    if not db_config.connect_mongoengine():
        raise Exception("Failed to connect MongoEngine")
    
    # Create indexes
    db_config.create_indexes()
    
    return app

app = create_app()

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Utility functions
def get_pagination_params():
    """Get pagination parameters from request"""
    page = request.args.get('page', 1, type=int)
    page_size = min(request.args.get('page_size', 20, type=int), 100)
    return page, page_size

def validate_required_fields(data, required_fields):
    """Validate required fields in request data"""
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    return True, ""

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'database': 'connected' if db_config.database is not None else 'disconnected'
    })

# ==================== MEDICATION ENDPOINTS ====================

@app.route('/api/medications', methods=['GET'])
def get_medications():
    """Get all medications with pagination and search"""
    page, page_size = get_pagination_params()
    search_query = request.args.get('search', '')
    
    if search_query:
        result = medication_repo.search(search_query, page, page_size)
    else:
        result = medication_repo.get_all(page, page_size)
    
    return jsonify(result)

@app.route('/api/medications/<medication_id>', methods=['GET'])
def get_medication(medication_id):
    """Get medication by ID"""
    medication = medication_repo.get_by_id(medication_id)
    if not medication:
        return jsonify({'error': 'Medication not found'}), 404
    return jsonify(medication)

@app.route('/api/medications', methods=['POST'])
def create_medication():
    """Create new medication"""
    data = request.get_json()
    
    required_fields = ['name', 'unit_price', 'quantity_in_stock']
    is_valid, error_msg = validate_required_fields(data, required_fields)
    if not is_valid:
        return jsonify({'error': error_msg}), 400
    
    try:
        medication = medication_repo.create(data)
        return jsonify(medication), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/medications/<medication_id>', methods=['PUT'])
def update_medication(medication_id):
    """Update medication"""
    data = request.get_json()
    
    try:
        medication = medication_repo.update(medication_id, data)
        if not medication:
            return jsonify({'error': 'Medication not found'}), 404
        return jsonify(medication)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/medications/<medication_id>', methods=['DELETE'])
def delete_medication(medication_id):
    """Delete medication"""
    success = medication_repo.delete(medication_id)
    if not success:
        return jsonify({'error': 'Medication not found'}), 404
    return jsonify({'message': 'Medication deleted successfully'})

@app.route('/api/medications/low-stock', methods=['GET'])
def get_low_stock_medications():
    """Get medications with low stock"""
    medications = medication_repo.get_low_stock()
    return jsonify({'data': medications})

@app.route('/api/medications/expiring', methods=['GET'])
def get_expiring_medications():
    """Get medications expiring soon"""
    days = request.args.get('days', 30, type=int)
    medications = medication_repo.get_expiring_soon(days)
    return jsonify({'data': medications})

# ==================== CUSTOMER ENDPOINTS ====================

@app.route('/api/customers', methods=['GET'])
def get_customers():
    """Get all customers with pagination and search"""
    page, page_size = get_pagination_params()
    search_query = request.args.get('search', '')
    
    if search_query:
        result = customer_repo.search(search_query, page, page_size)
    else:
        result = customer_repo.get_all(page, page_size)
    
    return jsonify(result)

@app.route('/api/customers/<customer_id>', methods=['GET'])
def get_customer(customer_id):
    """Get customer by ID"""
    customer = customer_repo.get_by_id(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    return jsonify(customer)

@app.route('/api/customers', methods=['POST'])
def create_customer():
    """Create new customer"""
    data = request.get_json()
    
    required_fields = ['first_name', 'last_name']
    is_valid, error_msg = validate_required_fields(data, required_fields)
    if not is_valid:
        return jsonify({'error': error_msg}), 400
    
    try:
        customer = customer_repo.create(data)
        return jsonify(customer), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/customers/<customer_id>', methods=['PUT'])
def update_customer(customer_id):
    """Update customer"""
    data = request.get_json()
    
    try:
        customer = customer_repo.update(customer_id, data)
        if not customer:
            return jsonify({'error': 'Customer not found'}), 404
        return jsonify(customer)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/customers/<customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    """Delete customer"""
    success = customer_repo.delete(customer_id)
    if not success:
        return jsonify({'error': 'Customer not found'}), 404
    return jsonify({'message': 'Customer deleted successfully'})

# ==================== PRESCRIPTION ENDPOINTS ====================

@app.route('/api/prescriptions', methods=['GET'])
def get_prescriptions():
    """Get all prescriptions with pagination"""
    page, page_size = get_pagination_params()
    result = prescription_repo.get_all(page, page_size)
    return jsonify(result)

@app.route('/api/prescriptions/<prescription_id>', methods=['GET'])
def get_prescription(prescription_id):
    """Get prescription by ID"""
    prescription = prescription_repo.get_by_id(prescription_id)
    if not prescription:
        return jsonify({'error': 'Prescription not found'}), 404
    return jsonify(prescription)

@app.route('/api/prescriptions', methods=['POST'])
def create_prescription():
    """Create new prescription"""
    data = request.get_json()
    
    required_fields = ['prescription_number', 'customer', 'doctor_name', 'issue_date']
    is_valid, error_msg = validate_required_fields(data, required_fields)
    if not is_valid:
        return jsonify({'error': error_msg}), 400
    
    try:
        prescription = prescription_repo.create(data)
        return jsonify(prescription), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/prescriptions/pending', methods=['GET'])
def get_pending_prescriptions():
    """Get all pending prescriptions"""
    prescriptions = prescription_repo.get_pending()
    return jsonify({'data': prescriptions})

# ==================== SALE ENDPOINTS ====================

@app.route('/api/sales', methods=['GET'])
def get_sales():
    """Get all sales with pagination"""
    page, page_size = get_pagination_params()
    result = sale_repo.get_all(page, page_size)
    return jsonify(result)

@app.route('/api/sales/<sale_id>', methods=['GET'])
def get_sale(sale_id):
    """Get sale by ID"""
    sale = sale_repo.get_by_id(sale_id)
    if not sale:
        return jsonify({'error': 'Sale not found'}), 404
    return jsonify(sale)

@app.route('/api/sales', methods=['POST'])
def create_sale():
    """Create new sale"""
    data = request.get_json()
    
    required_fields = ['invoice_number', 'user', 'items', 'total_amount', 'payment_method']
    is_valid, error_msg = validate_required_fields(data, required_fields)
    if not is_valid:
        return jsonify({'error': error_msg}), 400
    
    try:
        # Process sale and update inventory
        sale = sale_repo.create(data)
        
        # Update medication stock for each item
        for item in data.get('items', []):
            medication_repo.update_stock(
                medication_id=item['medication'],
                quantity_change=-item['quantity'],
                user_id=data['user'],
                transaction_type='sale',
                reference_id=sale['id']
            )
        
        return jsonify(sale), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/sales/reports/daily', methods=['GET'])
def get_daily_sales_report():
    """Get daily sales report"""
    date_str = request.args.get('date')
    if date_str:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    else:
        date = datetime.utcnow()
    
    report = sale_repo.get_daily_sales(date)
    return jsonify(report)

@app.route('/api/sales/reports/monthly', methods=['GET'])
def get_monthly_sales_report():
    """Get monthly sales report"""
    year = request.args.get('year', datetime.utcnow().year, type=int)
    month = request.args.get('month', datetime.utcnow().month, type=int)
    
    if month < 1 or month > 12:
        return jsonify({'error': 'Invalid month. Must be between 1 and 12'}), 400
    
    report = sale_repo.get_monthly_sales(year, month)
    return jsonify(report)

# ==================== USER ENDPOINTS ====================

@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users with pagination"""
    page, page_size = get_pagination_params()
    result = user_repo.get_all(page, page_size)
    return jsonify(result)

@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID"""
    user = user_repo.get_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    # Remove password hash from response
    user.pop('password_hash', None)
    return jsonify(user)

@app.route('/api/users', methods=['POST'])
def create_user():
    """Create new user"""
    data = request.get_json()
    
    required_fields = ['username', 'email', 'password_hash', 'role']
    is_valid, error_msg = validate_required_fields(data, required_fields)
    if not is_valid:
        return jsonify({'error': error_msg}), 400
    
    try:
        user = user_repo.create(data)
        # Remove password hash from response
        user.pop('password_hash', None)
        return jsonify(user), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)