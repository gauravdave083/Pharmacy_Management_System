"""
Backend package for Pharmacy Management System
"""

from .database.config import db_config
from .database.operations import (
    medication_repo, customer_repo, prescription_repo, 
    sale_repo, user_repo
)

__version__ = "1.0.0"