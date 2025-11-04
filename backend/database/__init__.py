"""
Database package for Pharmacy Management System
"""

from .config import db_config, get_database, get_collection
from .operations import (
    medication_repo, customer_repo, prescription_repo, 
    sale_repo, user_repo
)