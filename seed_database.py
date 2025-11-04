"""
Database seeding script for Pharmacy Management System
Populates the database with initial sample data
"""

import sys
import os
from datetime import datetime, timedelta
from decimal import Decimal

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database.config import db_config
from backend.models.pharmacy_models import (
    User, Medication, Customer, Prescription, Sale, Supplier,
    UserRole, PrescriptionStatus, PaymentMethod, PaymentStatus
)

def seed_database():
    """Seed the database with initial data"""
    
    print("🌱 Starting database seeding...")
    
    # Connect to database
    if not db_config.connect_to_mongodb():
        print("❌ Failed to connect to MongoDB")
        return False
    
    if not db_config.connect_mongoengine():
        print("❌ Failed to connect MongoEngine")
        return False
    
    try:
        # Clear existing data (for development only)
        print("🧹 Clearing existing data...")
        User.drop_collection()
        Medication.drop_collection()
        Customer.drop_collection()
        Prescription.drop_collection()
        Sale.drop_collection()
        Supplier.drop_collection()
        
        # Create indexes
        db_config.create_indexes()
        
        # Seed Users
        print("👥 Creating users...")
        users = [
            {
                'username': 'admin',
                'email': 'admin@pharmacy.com',
                'password_hash': 'hashed_password_admin',  # In real app, use proper hashing
                'role': UserRole.ADMIN,
                'full_name': 'System Administrator',
                'phone': '+1234567890',
                'is_active': True
            },
            {
                'username': 'pharmacist1',
                'email': 'pharmacist@pharmacy.com',
                'password_hash': 'hashed_password_pharmacist',
                'role': UserRole.PHARMACIST,
                'full_name': 'Dr. Sarah Johnson',
                'phone': '+1234567891',
                'is_active': True
            },
            {
                'username': 'cashier1',
                'email': 'cashier@pharmacy.com',
                'password_hash': 'hashed_password_cashier',
                'role': UserRole.CASHIER,
                'full_name': 'Mike Wilson',
                'phone': '+1234567892',
                'is_active': True
            }
        ]
        
        created_users = []
        for user_data in users:
            user = User(**user_data)
            user.save()
            created_users.append(user)
            print(f"   ✅ Created user: {user.username}")
        
        # Seed Suppliers
        print("🏭 Creating suppliers...")
        suppliers_data = [
            {
                'name': 'PharmaCorp Inc.',
                'contact_person': 'John Smith',
                'phone': '+1555000001',
                'email': 'contact@pharmacorp.com',
                'address': '123 Medical Drive, Healthcare City',
                'is_active': True
            },
            {
                'name': 'MedSupply Ltd.',
                'contact_person': 'Jane Doe',
                'phone': '+1555000002',
                'email': 'orders@medsupply.com',
                'address': '456 Pharma Street, Medicine Town',
                'is_active': True
            }
        ]
        
        created_suppliers = []
        for supplier_data in suppliers_data:
            supplier = Supplier(**supplier_data)
            supplier.save()
            created_suppliers.append(supplier)
            print(f"   ✅ Created supplier: {supplier.name}")
        
        # Seed Medications
        print("💊 Creating medications...")
        medications_data = [
            {
                'name': 'Paracetamol 500mg',
                'generic_name': 'Acetaminophen',
                'category': 'Analgesic',
                'manufacturer': 'PharmaCorp Inc.',
                'dosage_form': 'Tablet',
                'strength': '500mg',
                'unit_price': Decimal('1.50'),
                'quantity_in_stock': 500,
                'reorder_level': 100,
                'barcode': 'PAR500001',
                'expiry_date': datetime.utcnow() + timedelta(days=365),
                'batch_number': 'PAR2024001',
                'prescription_required': False,
                'supplier': created_suppliers[0]
            },
            {
                'name': 'Ibuprofen 400mg',
                'generic_name': 'Ibuprofen',
                'category': 'NSAID',
                'manufacturer': 'PharmaCorp Inc.',
                'dosage_form': 'Tablet',
                'strength': '400mg',
                'unit_price': Decimal('2.00'),
                'quantity_in_stock': 300,
                'reorder_level': 50,
                'barcode': 'IBU400001',
                'expiry_date': datetime.utcnow() + timedelta(days=540),
                'batch_number': 'IBU2024001',
                'prescription_required': False,
                'supplier': created_suppliers[0]
            },
            {
                'name': 'Amoxicillin 250mg',
                'generic_name': 'Amoxicillin',
                'category': 'Antibiotic',
                'manufacturer': 'MedSupply Ltd.',
                'dosage_form': 'Capsule',
                'strength': '250mg',
                'unit_price': Decimal('0.80'),
                'quantity_in_stock': 200,
                'reorder_level': 30,
                'barcode': 'AMX250001',
                'expiry_date': datetime.utcnow() + timedelta(days=720),
                'batch_number': 'AMX2024001',
                'prescription_required': True,
                'supplier': created_suppliers[1]
            },
            {
                'name': 'Cough Syrup 120ml',
                'generic_name': 'Dextromethorphan',
                'category': 'Cough Suppressant',
                'manufacturer': 'PharmaCorp Inc.',
                'dosage_form': 'Syrup',
                'strength': '15mg/5ml',
                'unit_price': Decimal('8.50'),
                'quantity_in_stock': 80,
                'reorder_level': 20,
                'barcode': 'COU120001',
                'expiry_date': datetime.utcnow() + timedelta(days=600),
                'batch_number': 'COU2024001',
                'prescription_required': False,
                'supplier': created_suppliers[0]
            },
            {
                'name': 'Insulin Injection 10ml',
                'generic_name': 'Human Insulin',
                'category': 'Antidiabetic',
                'manufacturer': 'MedSupply Ltd.',
                'dosage_form': 'Injection',
                'strength': '100IU/ml',
                'unit_price': Decimal('45.00'),
                'quantity_in_stock': 25,
                'reorder_level': 10,
                'barcode': 'INS100001',
                'expiry_date': datetime.utcnow() + timedelta(days=180),
                'batch_number': 'INS2024001',
                'prescription_required': True,
                'supplier': created_suppliers[1]
            }
        ]
        
        created_medications = []
        for med_data in medications_data:
            medication = Medication(**med_data)
            medication.save()
            created_medications.append(medication)
            print(f"   ✅ Created medication: {medication.name}")
        
        # Seed Customers
        print("👤 Creating customers...")
        customers_data = [
            {
                'first_name': 'John',
                'last_name': 'Doe',
                'date_of_birth': datetime(1985, 5, 15),
                'gender': 'male',
                'phone': '+1234567890',
                'email': 'john.doe@email.com',
                'address': '123 Main Street, Anytown, ST 12345',
                'allergies': 'Penicillin',
                'insurance_provider': 'HealthCare Plus',
                'insurance_number': 'HC123456789'
            },
            {
                'first_name': 'Jane',
                'last_name': 'Smith',
                'date_of_birth': datetime(1990, 8, 22),
                'gender': 'female',
                'phone': '+1234567891',
                'email': 'jane.smith@email.com',
                'address': '456 Oak Avenue, Somewhere, ST 67890',
                'allergies': 'None known',
                'insurance_provider': 'MediCare Pro',
                'insurance_number': 'MP987654321'
            },
            {
                'first_name': 'Robert',
                'last_name': 'Johnson',
                'date_of_birth': datetime(1975, 12, 3),
                'gender': 'male',
                'phone': '+1234567892',
                'email': 'robert.johnson@email.com',
                'address': '789 Pine Road, Elsewhere, ST 54321',
                'allergies': 'Sulfa drugs',
                'insurance_provider': 'Universal Health',
                'insurance_number': 'UH456789123'
            }
        ]
        
        created_customers = []
        for customer_data in customers_data:
            customer = Customer(**customer_data)
            customer.save()
            created_customers.append(customer)
            print(f"   ✅ Created customer: {customer.full_name}")
        
        # Seed Sample Prescriptions
        print("📋 Creating prescriptions...")
        prescriptions_data = [
            {
                'prescription_number': 'RX2024001',
                'customer': created_customers[0],
                'doctor_name': 'Dr. Emily Wilson',
                'doctor_license': 'MD12345',
                'issue_date': datetime.utcnow() - timedelta(days=2),
                'status': PrescriptionStatus.PENDING,
                'items': [
                    {
                        'medication': created_medications[2],  # Amoxicillin
                        'quantity': 30,
                        'dosage_instructions': 'Take 1 capsule three times daily with food for 10 days'
                    }
                ],
                'notes': 'Patient has bacterial infection'
            },
            {
                'prescription_number': 'RX2024002',
                'customer': created_customers[2],
                'doctor_name': 'Dr. Michael Brown',
                'doctor_license': 'MD67890',
                'issue_date': datetime.utcnow() - timedelta(days=1),
                'status': PrescriptionStatus.FILLED,
                'items': [
                    {
                        'medication': created_medications[4],  # Insulin
                        'quantity': 2,
                        'dosage_instructions': 'Inject 10 units subcutaneously before meals'
                    }
                ],
                'notes': 'Diabetes management'
            }
        ]
        
        created_prescriptions = []
        for prescription_data in prescriptions_data:
            prescription = Prescription(**prescription_data)
            prescription.save()
            created_prescriptions.append(prescription)
            print(f"   ✅ Created prescription: {prescription.prescription_number}")
        
        # Seed Sample Sales
        print("🛒 Creating sales...")
        sales_data = [
            {
                'invoice_number': 'INV2024001',
                'customer': created_customers[1],
                'user': created_users[2],  # Cashier
                'sale_date': datetime.utcnow() - timedelta(hours=6),
                'items': [
                    {
                        'medication': created_medications[0],  # Paracetamol
                        'quantity': 2,
                        'unit_price': Decimal('1.50'),
                        'total_price': Decimal('3.00')
                    },
                    {
                        'medication': created_medications[3],  # Cough Syrup
                        'quantity': 1,
                        'unit_price': Decimal('8.50'),
                        'total_price': Decimal('8.50')
                    }
                ],
                'subtotal': Decimal('11.50'),
                'tax_amount': Decimal('0.92'),
                'discount_amount': Decimal('0.00'),
                'total_amount': Decimal('12.42'),
                'payment_method': PaymentMethod.CASH,
                'payment_status': PaymentStatus.COMPLETED,
                'notes': 'Regular customer purchase'
            },
            {
                'invoice_number': 'INV2024002',
                'customer': created_customers[0],
                'user': created_users[1],  # Pharmacist
                'prescription': created_prescriptions[1],
                'sale_date': datetime.utcnow() - timedelta(hours=2),
                'items': [
                    {
                        'medication': created_medications[4],  # Insulin
                        'quantity': 2,
                        'unit_price': Decimal('45.00'),
                        'total_price': Decimal('90.00')
                    }
                ],
                'subtotal': Decimal('90.00'),
                'tax_amount': Decimal('7.20'),
                'discount_amount': Decimal('5.00'),
                'total_amount': Decimal('92.20'),
                'payment_method': PaymentMethod.INSURANCE,
                'payment_status': PaymentStatus.COMPLETED,
                'notes': 'Prescription fill - insurance claim submitted'
            }
        ]
        
        for sale_data in sales_data:
            sale = Sale(**sale_data)
            sale.save()
            print(f"   ✅ Created sale: {sale.invoice_number}")
        
        print("\n🎉 Database seeding completed successfully!")
        print(f"   👥 Created {len(created_users)} users")
        print(f"   🏭 Created {len(created_suppliers)} suppliers") 
        print(f"   💊 Created {len(created_medications)} medications")
        print(f"   👤 Created {len(created_customers)} customers")
        print(f"   📋 Created {len(created_prescriptions)} prescriptions")
        print(f"   🛒 Created {len(sales_data)} sales")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        return False
    
    finally:
        db_config.disconnect_mongodb()

if __name__ == "__main__":
    success = seed_database()
    if not success:
        sys.exit(1)