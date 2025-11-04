#!/usr/bin/env python3
"""
Production WSGI entry point for Pharmacy Management System API
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import the Flask app
from backend.app import app

if __name__ == "__main__":
    # Production server configuration
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    # Use Gunicorn in production, Flask dev server in development
    if os.environ.get('FLASK_ENV') == 'production':
        # This would be called by Gunicorn
        # gunicorn wsgi:app -b 0.0.0.0:5000 --workers 4
        pass
    else:
        # Development server
        app.run(host=host, port=port, debug=False)