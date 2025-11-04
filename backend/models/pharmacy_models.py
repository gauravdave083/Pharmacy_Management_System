"""
MongoDB Models for Pharmacy Management System
Using MongoEngine for ODM (Object Document Mapping)
"""

from mongoengine import Document, EmbeddedDocument, fields
from datetime import datetime
from enum import Enum

class UserRole(Enum):
    ADMIN = "admin"
    PHARMACIST = "pharmacist"
    CASHIER = "cashier"
    MANAGER = "manager"

class PrescriptionStatus(Enum):
    PENDING = "pending"
    FILLED = "filled"
    PARTIAL = "partial"
    CANCELLED = "cancelled"

class PaymentMethod(Enum):
    CASH = "cash"
    CARD = "card"
    INSURANCE = "insurance"
    DIGITAL = "digital"

class PaymentStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class User(Document):
    """User model for authentication and authorization"""
    username = fields.StringField(required=True, unique=True, max_length=50)
    email = fields.EmailField(required=True, unique=True)
    password_hash = fields.StringField(required=True)
    role = fields.EnumField(UserRole, required=True, default=UserRole.CASHIER)
    full_name = fields.StringField(max_length=100)
    phone = fields.StringField(max_length=20)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DateTimeField(default=datetime.utcnow)
    updated_at = fields.DateTimeField(default=datetime.utcnow)
    last_login = fields.DateTimeField()
    
    meta = {
        'collection': 'users',
        'indexes': ['username', 'email', 'role']
    }

class Supplier(Document):
    """Supplier model for medication suppliers"""
    name = fields.StringField(required=True, max_length=100)
    contact_person = fields.StringField(max_length=100)
    phone = fields.StringField(max_length=20)
    email = fields.EmailField()
    address = fields.StringField()
    is_active = fields.BooleanField(default=True)
    created_at = fields.DateTimeField(default=datetime.utcnow)
    updated_at = fields.DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'suppliers',
        'indexes': ['name', 'is_active']
    }

class Medication(Document):
    """Medication model for inventory management"""
    name = fields.StringField(required=True, max_length=200)
    generic_name = fields.StringField(max_length=200)
    category = fields.StringField(max_length=50)
    manufacturer = fields.StringField(max_length=100)
    dosage_form = fields.StringField(max_length=50)  # tablet, capsule, syrup, injection
    strength = fields.StringField(max_length=50)
    unit_price = fields.DecimalField(required=True, min_value=0, precision=2)
    quantity_in_stock = fields.IntField(required=True, min_value=0)
    reorder_level = fields.IntField(default=10)
    barcode = fields.StringField(unique=True, sparse=True, max_length=50)
    expiry_date = fields.DateTimeField()
    batch_number = fields.StringField(max_length=50)
    prescription_required = fields.BooleanField(default=False)
    supplier = fields.ReferenceField(Supplier)
    created_at = fields.DateTimeField(default=datetime.utcnow)
    updated_at = fields.DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'medications',
        'indexes': ['name', 'barcode', 'category', 'expiry_date', 'quantity_in_stock']
    }
    
    def is_low_stock(self):
        """Check if medication is low in stock"""
        return self.quantity_in_stock <= self.reorder_level
    
    def is_expired(self):
        """Check if medication is expired"""
        if self.expiry_date:
            return self.expiry_date < datetime.utcnow()
        return False

class Customer(Document):
    """Customer model for patient records"""
    first_name = fields.StringField(required=True, max_length=50)
    last_name = fields.StringField(required=True, max_length=50)
    date_of_birth = fields.DateTimeField()
    gender = fields.StringField(max_length=10, choices=['male', 'female', 'other'])
    phone = fields.StringField(max_length=20)
    email = fields.EmailField()
    address = fields.StringField()
    allergies = fields.StringField()
    insurance_provider = fields.StringField(max_length=100)
    insurance_number = fields.StringField(max_length=50)
    created_at = fields.DateTimeField(default=datetime.utcnow)
    updated_at = fields.DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'customers',
        'indexes': ['phone', 'email', 'first_name', 'last_name']
    }
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class PrescriptionItem(EmbeddedDocument):
    """Embedded document for prescription items"""
    medication = fields.ReferenceField(Medication, required=True)
    quantity = fields.IntField(required=True, min_value=1)
    dosage_instructions = fields.StringField()
    created_at = fields.DateTimeField(default=datetime.utcnow)

class Prescription(Document):
    """Prescription model for prescription management"""
    prescription_number = fields.StringField(required=True, unique=True, max_length=50)
    customer = fields.ReferenceField(Customer, required=True)
    doctor_name = fields.StringField(required=True, max_length=100)
    doctor_license = fields.StringField(max_length=50)
    issue_date = fields.DateTimeField(required=True)
    status = fields.EnumField(PrescriptionStatus, default=PrescriptionStatus.PENDING)
    items = fields.ListField(fields.EmbeddedDocumentField(PrescriptionItem))
    notes = fields.StringField()
    created_at = fields.DateTimeField(default=datetime.utcnow)
    updated_at = fields.DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'prescriptions',
        'indexes': ['prescription_number', 'customer', 'issue_date', 'status']
    }

class SaleItem(EmbeddedDocument):
    """Embedded document for sale items"""
    medication = fields.ReferenceField(Medication, required=True)
    quantity = fields.IntField(required=True, min_value=1)
    unit_price = fields.DecimalField(required=True, min_value=0, precision=2)
    total_price = fields.DecimalField(required=True, min_value=0, precision=2)
    created_at = fields.DateTimeField(default=datetime.utcnow)

class Sale(Document):
    """Sale model for transaction management"""
    invoice_number = fields.StringField(required=True, unique=True, max_length=50)
    customer = fields.ReferenceField(Customer)
    user = fields.ReferenceField(User, required=True)  # Cashier/user who processed the sale
    prescription = fields.ReferenceField(Prescription)  # If sale is from prescription
    sale_date = fields.DateTimeField(default=datetime.utcnow)
    items = fields.ListField(fields.EmbeddedDocumentField(SaleItem))
    subtotal = fields.DecimalField(required=True, min_value=0, precision=2)
    tax_amount = fields.DecimalField(default=0, min_value=0, precision=2)
    discount_amount = fields.DecimalField(default=0, min_value=0, precision=2)
    total_amount = fields.DecimalField(required=True, min_value=0, precision=2)
    payment_method = fields.EnumField(PaymentMethod, required=True)
    payment_status = fields.EnumField(PaymentStatus, default=PaymentStatus.COMPLETED)
    notes = fields.StringField()
    created_at = fields.DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'sales',
        'indexes': ['invoice_number', 'customer', 'user', 'sale_date', 'payment_status']
    }

class InventoryTransaction(Document):
    """Model for tracking inventory changes"""
    medication = fields.ReferenceField(Medication, required=True)
    transaction_type = fields.StringField(required=True, choices=['purchase', 'sale', 'adjustment', 'return'])
    quantity_change = fields.IntField(required=True)  # Positive for additions, negative for reductions
    previous_quantity = fields.IntField(required=True)
    new_quantity = fields.IntField(required=True)
    reference_id = fields.StringField()  # Reference to sale, purchase order, etc.
    user = fields.ReferenceField(User, required=True)
    notes = fields.StringField()
    created_at = fields.DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'inventory_transactions',
        'indexes': ['medication', 'transaction_type', 'created_at', 'user']
    }

class PurchaseOrder(Document):
    """Purchase order model for supplier orders"""
    order_number = fields.StringField(required=True, unique=True, max_length=50)
    supplier = fields.ReferenceField(Supplier, required=True)
    order_date = fields.DateTimeField(default=datetime.utcnow)
    expected_delivery_date = fields.DateTimeField()
    status = fields.StringField(default='pending', choices=['pending', 'ordered', 'received', 'cancelled'])
    items = fields.ListField(fields.DictField())  # List of {medication_id, quantity, unit_price}
    total_amount = fields.DecimalField(min_value=0, precision=2)
    received_date = fields.DateTimeField()
    created_by = fields.ReferenceField(User, required=True)
    notes = fields.StringField()
    created_at = fields.DateTimeField(default=datetime.utcnow)
    updated_at = fields.DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'purchase_orders',
        'indexes': ['order_number', 'supplier', 'order_date', 'status']
    }