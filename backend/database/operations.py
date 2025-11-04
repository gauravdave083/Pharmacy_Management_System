"""
Database Operations for Pharmacy Management System
CRUD operations using PyMongo and MongoEngine
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from mongoengine.errors import NotUniqueError, ValidationError

from backend.models.pharmacy_models import (
    User, Medication, Customer, Prescription, Sale, 
    Supplier, InventoryTransaction, PurchaseOrder,
    UserRole, PrescriptionStatus, PaymentMethod, PaymentStatus
)
from backend.database.config import get_database, get_collection

class BaseRepository:
    """Base repository class with common CRUD operations"""
    
    def __init__(self, model_class, collection_name):
        self.model_class = model_class
        self.collection_name = collection_name
        self.collection = get_collection(collection_name)
    
    def create(self, data: Dict[Any, Any]) -> Dict[Any, Any]:
        """Create a new document"""
        try:
            # Create using MongoEngine for validation
            instance = self.model_class(**data)
            instance.save()
            return self._to_dict(instance)
        except (NotUniqueError, ValidationError) as e:
            raise ValueError(f"Validation error: {str(e)}")
    
    def get_by_id(self, doc_id: str) -> Optional[Dict[Any, Any]]:
        """Get document by ID"""
        try:
            instance = self.model_class.objects(id=doc_id).first()
            return self._to_dict(instance) if instance else None
        except Exception as e:
            return None
    
    def get_all(self, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """Get all documents with pagination"""
        skip = (page - 1) * page_size
        instances = self.model_class.objects.skip(skip).limit(page_size)
        total = self.model_class.objects.count()
        
        return {
            "data": [self._to_dict(instance) for instance in instances],
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total": total,
                "pages": (total + page_size - 1) // page_size
            }
        }
    
    def update(self, doc_id: str, data: Dict[Any, Any]) -> Optional[Dict[Any, Any]]:
        """Update document by ID"""
        try:
            instance = self.model_class.objects(id=doc_id).first()
            if not instance:
                return None
            
            for key, value in data.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            
            instance.updated_at = datetime.utcnow()
            instance.save()
            return self._to_dict(instance)
        except Exception as e:
            raise ValueError(f"Update error: {str(e)}")
    
    def delete(self, doc_id: str) -> bool:
        """Delete document by ID"""
        try:
            instance = self.model_class.objects(id=doc_id).first()
            if instance:
                instance.delete()
                return True
            return False
        except Exception as e:
            return False
    
    def _to_dict(self, instance) -> Dict[Any, Any]:
        """Convert MongoEngine document to dictionary"""
        if not instance:
            return {}
        
        data = instance.to_mongo().to_dict()
        data['id'] = str(data.pop('_id'))
        return data

class MedicationRepository(BaseRepository):
    """Repository for Medication operations"""
    
    def __init__(self):
        super().__init__(Medication, 'medications')
    
    def search(self, query: str, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """Search medications by name, generic name, or category"""
        skip = (page - 1) * page_size
        
        instances = Medication.objects(
            name__icontains=query
        ).skip(skip).limit(page_size)
        
        total = Medication.objects(name__icontains=query).count()
        
        return {
            "data": [self._to_dict(instance) for instance in instances],
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total": total,
                "pages": (total + page_size - 1) // page_size
            }
        }
    
    def get_low_stock(self) -> List[Dict[Any, Any]]:
        """Get medications with low stock"""
        # Using PyMongo for complex query
        pipeline = [
            {
                "$addFields": {
                    "is_low_stock": {
                        "$lte": ["$quantity_in_stock", "$reorder_level"]
                    }
                }
            },
            {
                "$match": {"is_low_stock": True}
            }
        ]
        
        results = list(self.collection.aggregate(pipeline))
        for result in results:
            result['id'] = str(result.pop('_id'))
        
        return results
    
    def get_expiring_soon(self, days: int = 30) -> List[Dict[Any, Any]]:
        """Get medications expiring within specified days"""
        expiry_threshold = datetime.utcnow() + timedelta(days=days)
        
        instances = Medication.objects(
            expiry_date__lte=expiry_threshold,
            expiry_date__gte=datetime.utcnow()
        )
        
        return [self._to_dict(instance) for instance in instances]
    
    def update_stock(self, medication_id: str, quantity_change: int, user_id: str, 
                    transaction_type: str = 'adjustment', reference_id: str = None) -> bool:
        """Update medication stock and log transaction"""
        try:
            medication = Medication.objects(id=medication_id).first()
            if not medication:
                return False
            
            previous_quantity = medication.quantity_in_stock
            new_quantity = previous_quantity + quantity_change
            
            if new_quantity < 0:
                raise ValueError("Insufficient stock")
            
            # Update medication stock
            medication.quantity_in_stock = new_quantity
            medication.updated_at = datetime.utcnow()
            medication.save()
            
            # Log inventory transaction
            InventoryTransaction(
                medication=medication,
                transaction_type=transaction_type,
                quantity_change=quantity_change,
                previous_quantity=previous_quantity,
                new_quantity=new_quantity,
                reference_id=reference_id,
                user=ObjectId(user_id)
            ).save()
            
            return True
        except Exception as e:
            return False

class CustomerRepository(BaseRepository):
    """Repository for Customer operations"""
    
    def __init__(self):
        super().__init__(Customer, 'customers')
    
    def search(self, query: str, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """Search customers by name, phone, or email"""
        skip = (page - 1) * page_size
        
        instances = Customer.objects(
            first_name__icontains=query
        ).skip(skip).limit(page_size)
        
        total = Customer.objects(first_name__icontains=query).count()
        
        return {
            "data": [self._to_dict(instance) for instance in instances],
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total": total,
                "pages": (total + page_size - 1) // page_size
            }
        }
    
    def get_by_phone(self, phone: str) -> Optional[Dict[Any, Any]]:
        """Get customer by phone number"""
        instance = Customer.objects(phone=phone).first()
        return self._to_dict(instance) if instance else None

class PrescriptionRepository(BaseRepository):
    """Repository for Prescription operations"""
    
    def __init__(self):
        super().__init__(Prescription, 'prescriptions')
    
    def get_by_customer(self, customer_id: str, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """Get prescriptions by customer"""
        skip = (page - 1) * page_size
        
        instances = Prescription.objects(
            customer=ObjectId(customer_id)
        ).skip(skip).limit(page_size).order_by('-created_at')
        
        total = Prescription.objects(customer=ObjectId(customer_id)).count()
        
        return {
            "data": [self._to_dict(instance) for instance in instances],
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total": total,
                "pages": (total + page_size - 1) // page_size
            }
        }
    
    def get_pending(self) -> List[Dict[Any, Any]]:
        """Get all pending prescriptions"""
        instances = Prescription.objects(status=PrescriptionStatus.PENDING)
        return [self._to_dict(instance) for instance in instances]

class SaleRepository(BaseRepository):
    """Repository for Sale operations"""
    
    def __init__(self):
        super().__init__(Sale, 'sales')
    
    def get_daily_sales(self, date: datetime = None) -> Dict[str, Any]:
        """Get sales for a specific date"""
        if not date:
            date = datetime.utcnow()
        
        start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)
        
        # Using PyMongo for aggregation
        pipeline = [
            {
                "$match": {
                    "sale_date": {
                        "$gte": start_date,
                        "$lt": end_date
                    }
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total_sales": {"$sum": "$total_amount"},
                    "total_transactions": {"$sum": 1},
                    "average_sale": {"$avg": "$total_amount"}
                }
            }
        ]
        
        results = list(self.collection.aggregate(pipeline))
        if results:
            result = results[0]
            result.pop('_id')
            return result
        
        return {
            "total_sales": 0,
            "total_transactions": 0,
            "average_sale": 0
        }
    
    def get_monthly_sales(self, year: int, month: int) -> Dict[str, Any]:
        """Get sales for a specific month"""
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
        
        pipeline = [
            {
                "$match": {
                    "sale_date": {
                        "$gte": start_date,
                        "$lt": end_date
                    }
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total_sales": {"$sum": "$total_amount"},
                    "total_transactions": {"$sum": 1},
                    "average_sale": {"$avg": "$total_amount"}
                }
            }
        ]
        
        results = list(self.collection.aggregate(pipeline))
        if results:
            result = results[0]
            result.pop('_id')
            return result
        
        return {
            "total_sales": 0,
            "total_transactions": 0,
            "average_sale": 0
        }

class UserRepository(BaseRepository):
    """Repository for User operations"""
    
    def __init__(self):
        super().__init__(User, 'users')
    
    def get_by_username(self, username: str) -> Optional[Dict[Any, Any]]:
        """Get user by username"""
        instance = User.objects(username=username).first()
        return self._to_dict(instance) if instance else None
    
    def get_by_email(self, email: str) -> Optional[Dict[Any, Any]]:
        """Get user by email"""
        instance = User.objects(email=email).first()
        return self._to_dict(instance) if instance else None

# Repository instances
medication_repo = MedicationRepository()
customer_repo = CustomerRepository()
prescription_repo = PrescriptionRepository()
sale_repo = SaleRepository()
user_repo = UserRepository()