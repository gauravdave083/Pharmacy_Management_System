"""
API Client for Pharmacy Management System
Handles all API communications between Streamlit frontend and Flask backend
"""

import requests
import streamlit as st
from typing import Dict, List, Optional, Any
import pandas as pd
from datetime import datetime

class PharmacyAPIClient:
    """API client for pharmacy management system"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Make HTTP request with error handling"""
        try:
            url = f"{self.base_url}{endpoint}"
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            st.error("🔌 Cannot connect to API server. Please ensure the backend is running on port 5000.")
            return None
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                st.error(f"❌ Resource not found: {endpoint}")
            elif response.status_code == 400:
                error_msg = response.json().get('error', 'Bad request')
                st.error(f"❌ Request error: {error_msg}")
            else:
                st.error(f"❌ HTTP Error {response.status_code}: {e}")
            return None
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Request failed: {str(e)}")
            return None
        except ValueError as e:
            st.error(f"❌ Invalid JSON response: {str(e)}")
            return None
    
    def health_check(self) -> bool:
        """Check if API server is healthy"""
        result = self._make_request('GET', '/health')
        return result is not None and result.get('status') == 'healthy'
    
    # ==================== MEDICATION METHODS ====================
    
    def get_medications(self, page: int = 1, page_size: int = 20, search: str = "") -> Optional[Dict[str, Any]]:
        """Get medications with pagination and search"""
        params = {'page': page, 'page_size': page_size}
        if search:
            params['search'] = search
        
        return self._make_request('GET', '/api/medications', params=params)
    
    def get_medication(self, medication_id: str) -> Optional[Dict[str, Any]]:
        """Get single medication by ID"""
        return self._make_request('GET', f'/api/medications/{medication_id}')
    
    def create_medication(self, medication_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create new medication"""
        return self._make_request('POST', '/api/medications', json=medication_data)
    
    def update_medication(self, medication_id: str, medication_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update existing medication"""
        return self._make_request('PUT', f'/api/medications/{medication_id}', json=medication_data)
    
    def delete_medication(self, medication_id: str) -> bool:
        """Delete medication"""
        result = self._make_request('DELETE', f'/api/medications/{medication_id}')
        return result is not None
    
    def get_low_stock_medications(self) -> Optional[List[Dict[str, Any]]]:
        """Get medications with low stock"""
        result = self._make_request('GET', '/api/medications/low-stock')
        return result.get('data') if result else None
    
    def get_expiring_medications(self, days: int = 30) -> Optional[List[Dict[str, Any]]]:
        """Get medications expiring soon"""
        result = self._make_request('GET', '/api/medications/expiring', params={'days': days})
        return result.get('data') if result else None
    
    # ==================== CUSTOMER METHODS ====================
    
    def get_customers(self, page: int = 1, page_size: int = 20, search: str = "") -> Optional[Dict[str, Any]]:
        """Get customers with pagination and search"""
        params = {'page': page, 'page_size': page_size}
        if search:
            params['search'] = search
        
        return self._make_request('GET', '/api/customers', params=params)
    
    def get_customer(self, customer_id: str) -> Optional[Dict[str, Any]]:
        """Get single customer by ID"""
        return self._make_request('GET', f'/api/customers/{customer_id}')
    
    def create_customer(self, customer_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create new customer"""
        return self._make_request('POST', '/api/customers', json=customer_data)
    
    def update_customer(self, customer_id: str, customer_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update existing customer"""
        return self._make_request('PUT', f'/api/customers/{customer_id}', json=customer_data)
    
    def delete_customer(self, customer_id: str) -> bool:
        """Delete customer"""
        result = self._make_request('DELETE', f'/api/customers/{customer_id}')
        return result is not None
    
    # ==================== SALES METHODS ====================
    
    def get_sales(self, page: int = 1, page_size: int = 20) -> Optional[Dict[str, Any]]:
        """Get sales with pagination"""
        params = {'page': page, 'page_size': page_size}
        return self._make_request('GET', '/api/sales', params=params)
    
    def get_sale(self, sale_id: str) -> Optional[Dict[str, Any]]:
        """Get single sale by ID"""
        return self._make_request('GET', f'/api/sales/{sale_id}')
    
    def create_sale(self, sale_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create new sale"""
        return self._make_request('POST', '/api/sales', json=sale_data)
    
    def get_daily_sales_report(self, date: str = None) -> Optional[Dict[str, Any]]:
        """Get daily sales report"""
        params = {}
        if date:
            params['date'] = date
        return self._make_request('GET', '/api/sales/reports/daily', params=params)
    
    def get_monthly_sales_report(self, year: int = None, month: int = None) -> Optional[Dict[str, Any]]:
        """Get monthly sales report"""
        params = {}
        if year:
            params['year'] = year
        if month:
            params['month'] = month
        return self._make_request('GET', '/api/sales/reports/monthly', params=params)
    
    # ==================== PRESCRIPTION METHODS ====================
    
    def get_prescriptions(self, page: int = 1, page_size: int = 20) -> Optional[Dict[str, Any]]:
        """Get prescriptions with pagination"""
        params = {'page': page, 'page_size': page_size}
        return self._make_request('GET', '/api/prescriptions', params=params)
    
    def get_prescription(self, prescription_id: str) -> Optional[Dict[str, Any]]:
        """Get single prescription by ID"""
        return self._make_request('GET', f'/api/prescriptions/{prescription_id}')
    
    def create_prescription(self, prescription_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create new prescription"""
        return self._make_request('POST', '/api/prescriptions', json=prescription_data)
    
    def get_pending_prescriptions(self) -> Optional[List[Dict[str, Any]]]:
        """Get all pending prescriptions"""
        result = self._make_request('GET', '/api/prescriptions/pending')
        return result.get('data') if result else None
    
    # ==================== USER METHODS ====================
    
    def get_users(self, page: int = 1, page_size: int = 20) -> Optional[Dict[str, Any]]:
        """Get users with pagination"""
        params = {'page': page, 'page_size': page_size}
        return self._make_request('GET', '/api/users', params=params)
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get single user by ID"""
        return self._make_request('GET', f'/api/users/{user_id}')
    
    def create_user(self, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create new user"""
        return self._make_request('POST', '/api/users', json=user_data)
    
    # ==================== UTILITY METHODS ====================
    
    def medications_to_dataframe(self, medications_data: Dict[str, Any]) -> pd.DataFrame:
        """Convert medications API response to DataFrame"""
        if not medications_data or 'data' not in medications_data:
            return pd.DataFrame()
        
        medications = medications_data['data']
        if not medications:
            return pd.DataFrame()
        
        # Convert to DataFrame and format for display
        df = pd.DataFrame(medications)
        
        # Rename columns for better display
        column_mapping = {
            'name': 'Item',
            'quantity_in_stock': 'Quantity',
            'unit_price': 'Price',
            'dosage_form': 'Type'
        }
        
        # Select and rename relevant columns
        display_columns = ['name', 'quantity_in_stock', 'unit_price', 'dosage_form']
        available_columns = [col for col in display_columns if col in df.columns]
        
        if available_columns:
            df_display = df[available_columns].copy()
            df_display = df_display.rename(columns=column_mapping)
            
            # Add emoji for type
            if 'Type' in df_display.columns:
                df_display['Type'] = df_display['Type'].apply(self._add_type_emoji)
            
            # Format price
            if 'Price' in df_display.columns:
                df_display['Price'] = df_display['Price'].astype(float)
            
            return df_display
        
        return df
    
    def _add_type_emoji(self, dosage_form: str) -> str:
        """Add emoji to dosage form"""
        if not dosage_form:
            return "Other 🛒"
        
        dosage_form_lower = str(dosage_form).lower()
        
        if any(word in dosage_form_lower for word in ['tablet', 'capsule']):
            return f"Tablet 💊"
        elif 'syrup' in dosage_form_lower:
            return f"Syrup 🥤"
        elif 'injection' in dosage_form_lower:
            return f"Injection 💉"
        else:
            return f"Other 🛒"

# Global API client instance
@st.cache_resource
def get_api_client():
    """Get cached API client instance"""
    return PharmacyAPIClient()

# Helper functions for Streamlit
def check_api_connection():
    """Check API connection and show status"""
    api_client = get_api_client()
    
    if api_client.health_check():
        st.success("✅ Connected to pharmacy management API")
        return True
    else:
        st.error("❌ Cannot connect to API. Please ensure the backend server is running.")
        st.info("💡 To start the backend server, run: `python backend/app.py`")
        return False

def handle_api_error(func):
    """Decorator to handle API errors gracefully"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            return None
    return wrapper