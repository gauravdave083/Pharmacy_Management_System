# MongoDB Configuration for Pharmacy Management System
import os
from pymongo import MongoClient
from mongoengine import connect, disconnect
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MongoDBConfig:
    """MongoDB Configuration Class"""
    
    def __init__(self):
        self.MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        self.DATABASE_NAME = os.getenv('DATABASE_NAME', 'pharmacy_management')
        self.client = None
        self.database = None
    
    def connect_to_mongodb(self):
        """Connect to MongoDB using PyMongo"""
        try:
            self.client = MongoClient(self.MONGODB_URI)
            self.database = self.client[self.DATABASE_NAME]
            # Test connection
            self.client.admin.command('ping')
            print(f"✅ Connected to MongoDB: {self.DATABASE_NAME}")
            return True
        except Exception as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            return False
    
    def connect_mongoengine(self):
        """Connect to MongoDB using MongoEngine"""
        try:
            connect(
                db=self.DATABASE_NAME,
                host=self.MONGODB_URI,
                alias='default'
            )
            print(f"✅ MongoEngine connected to: {self.DATABASE_NAME}")
            return True
        except Exception as e:
            print(f"❌ Failed to connect MongoEngine: {e}")
            return False
    
    def disconnect_mongodb(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
        disconnect(alias='default')
        print("🔌 Disconnected from MongoDB")
    
    def get_collection(self, collection_name):
        """Get a specific collection"""
        if self.database is not None:
            return self.database[collection_name]
        return None
    
    def create_indexes(self):
        """Create indexes for better performance"""
        try:
            if self.database is None:
                print("❌ Database not connected, cannot create indexes")
                return False
                
            # Helper function to create index safely
            def safe_create_index(collection, field_spec, **kwargs):
                try:
                    collection.create_index(field_spec, **kwargs)
                except Exception as idx_error:
                    # Ignore "index already exists" errors
                    if "already exists" not in str(idx_error).lower():
                        print(f"Warning: Could not create index {field_spec}: {idx_error}")
                
            # Medications collection indexes
            medications = self.get_collection('medications')
            if medications is not None:
                safe_create_index(medications, "name")
                safe_create_index(medications, "barcode", unique=True, sparse=True)
                safe_create_index(medications, "expiry_date")
            
            # Customers collection indexes
            customers = self.get_collection('customers')
            if customers is not None:
                safe_create_index(customers, "phone")
                safe_create_index(customers, "email", sparse=True)
            
            # Prescriptions collection indexes
            prescriptions = self.get_collection('prescriptions')
            if prescriptions is not None:
                safe_create_index(prescriptions, "prescription_number", unique=True)
                safe_create_index(prescriptions, "customer_id")
                safe_create_index(prescriptions, "issue_date")
            
            # Sales collection indexes
            sales = self.get_collection('sales')
            if sales is not None:
                safe_create_index(sales, "invoice_number", unique=True)
                safe_create_index(sales, "customer_id")
                safe_create_index(sales, "sale_date")
            
            # Users collection indexes
            users = self.get_collection('users')
            if users is not None:
                safe_create_index(users, "username", unique=True)
                safe_create_index(users, "email", unique=True)
            
            print("✅ Database indexes processed successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to create indexes: {e}")
            return False

# Global database configuration instance
db_config = MongoDBConfig()

def get_database():
    """Get database instance"""
    return db_config.database

def get_collection(collection_name):
    """Get a specific collection"""
    return db_config.get_collection(collection_name)