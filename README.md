# Pharmacy_Management_System

# Pharmacy Management System

A comprehensive pharmacy management system built with Python and SQL, designed to streamline medication inventory, prescription processing, sales tracking, and customer management operations.

## Features

### Core Functionality
- **Inventory Management**: Track medication stock levels, expiration dates, and reorder points
- **Prescription Processing**: Handle electronic and physical prescriptions with validation
- **Sales & Billing**: Generate invoices, process payments, and track transactions
- **Customer Management**: Maintain customer profiles and prescription history
- **Supplier Management**: Track suppliers, purchase orders, and deliveries
- **Reporting & Analytics**: Generate sales reports, inventory reports, and business insights

### Additional Features
- User authentication and role-based access control
- Low stock alerts and expiration notifications
- Barcode scanning support
- Multi-location support
- Drug interaction checking
- Insurance claim processing

## Technology Stack

### Backend
- **Language**: Python 3.9+
- **Framework**: Flask / Django
- **Database**: MySQL
- **API**: RESTful API

### Frontend
- **Framework**: Streamlit (Web UI)
- **Alternative**: Flask with Jinja2 templates
- **Reporting**: Matplotlib / Plotly for data visualization

### Additional Libraries
- **Authentication**: Flask-Login / Django Authentication
- **PDF Generation**: ReportLab / WeasyPrint
- **Excel Export**: openpyxl / xlsxwriter
- **Email**: smtplib / Flask-Mail
- **Testing**: pytest / unittest
- **Database Migrations**: Alembic / Django Migrations

## Getting Started

### Prerequisites
```bash
# Required software
- Python 3.9 or higher
- PostgreSQL 13+ or MySQL 8+
- pip (Python package manager)
- virtualenv (recommended)
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/pharmacy-management.git
cd pharmacy-management
```

2. **Create and activate virtual environment**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Database Setup**
```bash
# Create database
# PostgreSQL:
createdb pharmacy_db

# MySQL:
mysql -u root -p
CREATE DATABASE pharmacy_db;
```

5. **Configure environment variables**
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use any text editor
```

6. **Run database migrations**
```bash
# If using Flask with Alembic:
flask db upgrade

# If using Django:
python manage.py migrate
```

7. **Create admin user**
```bash
python create_admin.py
# Follow prompts to create admin account
```

8. **Run the application**
```bash
# Flask:
python app.py
# or
flask run

# Django:
python manage.py runserver

# Tkinter (Desktop):
python main.py
```

### Environment Variables

Create a `.env` file in the root directory:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=pharmacy_db
DB_USER=your_username
DB_PASSWORD=your_password
DATABASE_URL=postgresql://user:password@localhost:5432/pharmacy_db

# Application Settings
SECRET_KEY=your_secret_key_here
FLASK_ENV=development
DEBUG=True

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_email_password
MAIL_USE_TLS=True

# Payment Gateway (Optional)
PAYMENT_API_KEY=your_payment_gateway_key

# Application Port
PORT=5000
```

## Project Structure

```
pharmacy-management/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── medication.py
│   │   ├── prescription.py
│   │   ├── sale.py
│   │   └── customer.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── auth_controller.py
│   │   ├── medication_controller.py
│   │   ├── prescription_controller.py
│   │   └── sales_controller.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── dashboard.py
│   │   ├── inventory.py
│   │   └── reports.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── validators.py
│   │   └── helpers.py
│   └── static/
│       ├── css/
│       ├── js/
│       └── images/
├── migrations/
├── tests/
│   ├── test_models.py
│   ├── test_controllers.py
│   └── test_utils.py
├── config.py
├── requirements.txt
├── app.py
├── .env.example
├── .gitignore
├── README.md
└── LICENSE
```

## Dependencies (requirements.txt)

```txt
# Core Framework
Flask==3.0.0
# or Django==4.2.0

# Database
psycopg2-binary==2.9.9  # PostgreSQL
# or PyMySQL==1.1.0  # MySQL
SQLAlchemy==2.0.23
alembic==1.13.0

# Authentication
Flask-Login==0.6.3
werkzeug==3.0.1
PyJWT==2.8.0

# Forms and Validation
Flask-WTF==1.2.1
WTForms==3.1.1

# Database Migrations
Flask-Migrate==4.0.5

# PDF Generation
reportlab==4.0.7
WeasyPrint==60.1

# Excel Operations
openpyxl==3.1.2
xlsxwriter==3.1.9

# Email
Flask-Mail==0.9.1

# Data Visualization
matplotlib==3.8.2
plotly==5.18.0

# GUI (if using Tkinter)
ttkbootstrap==1.10.1

# Web UI (alternative)
streamlit==1.29.0

# Barcode
python-barcode==0.15.1

# Environment Variables
python-dotenv==1.0.0

# Date and Time
python-dateutil==2.8.2

# Testing
pytest==7.4.3
pytest-cov==4.1.0

# Development
black==23.12.1
flake8==6.1.0
```

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    full_name VARCHAR(100),
    phone VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Medications Table
```sql
CREATE TABLE medications (
    medication_id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    generic_name VARCHAR(200),
    category VARCHAR(50),
    manufacturer VARCHAR(100),
    dosage_form VARCHAR(50),
    strength VARCHAR(50),
    unit_price DECIMAL(10, 2) NOT NULL,
    quantity_in_stock INTEGER NOT NULL,
    reorder_level INTEGER,
    barcode VARCHAR(50) UNIQUE,
    expiry_date DATE,
    batch_number VARCHAR(50),
    prescription_required BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Customers Table
```sql
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE,
    gender VARCHAR(10),
    phone VARCHAR(20),
    email VARCHAR(100),
    address TEXT,
    allergies TEXT,
    insurance_provider VARCHAR(100),
    insurance_number VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Prescriptions Table
```sql
CREATE TABLE prescriptions (
    prescription_id SERIAL PRIMARY KEY,
    prescription_number VARCHAR(50) UNIQUE NOT NULL,
    customer_id INTEGER REFERENCES customers(customer_id),
    doctor_name VARCHAR(100) NOT NULL,
    doctor_license VARCHAR(50),
    issue_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Prescription Items Table
```sql
CREATE TABLE prescription_items (
    item_id SERIAL PRIMARY KEY,
    prescription_id INTEGER REFERENCES prescriptions(prescription_id),
    medication_id INTEGER REFERENCES medications(medication_id),
    quantity INTEGER NOT NULL,
    dosage_instructions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Sales Table
```sql
CREATE TABLE sales (
    sale_id SERIAL PRIMARY KEY,
    invoice_number VARCHAR(50) UNIQUE NOT NULL,
    customer_id INTEGER REFERENCES customers(customer_id),
    user_id INTEGER REFERENCES users(user_id),
    prescription_id INTEGER REFERENCES prescriptions(prescription_id),
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    subtotal DECIMAL(10, 2) NOT NULL,
    tax_amount DECIMAL(10, 2) DEFAULT 0,
    discount_amount DECIMAL(10, 2) DEFAULT 0,
    total_amount DECIMAL(10, 2) NOT NULL,
    payment_method VARCHAR(20),
    payment_status VARCHAR(20) DEFAULT 'completed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Sale Items Table
```sql
CREATE TABLE sale_items (
    item_id SERIAL PRIMARY KEY,
    sale_id INTEGER REFERENCES sales(sale_id),
    medication_id INTEGER REFERENCES medications(medication_id),
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Suppliers Table
```sql
CREATE TABLE suppliers (
    supplier_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact_person VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100),
    address TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## API Endpoints (Flask Example)

### Authentication
```python
POST /api/auth/login          # User login
POST /api/auth/logout         # User logout
POST /api/auth/register       # User registration
GET  /api/auth/profile        # Get user profile
```

### Medications
```python
GET    /api/medications              # Get all medications
GET    /api/medications/<id>         # Get medication by ID
POST   /api/medications              # Add new medication
PUT    /api/medications/<id>         # Update medication
DELETE /api/medications/<id>         # Delete medication
GET    /api/medications/low-stock    # Get low stock medications
GET    /api/medications/expiring     # Get expiring medications
```

### Prescriptions
```python
GET  /api/prescriptions              # Get all prescriptions
POST /api/prescriptions              # Create prescription
GET  /api/prescriptions/<id>         # Get prescription details
PUT  /api/prescriptions/<id>         # Update prescription
```

### Sales
```python
GET  /api/sales                      # Get sales records
POST /api/sales                      # Process new sale
GET  /api/sales/<id>                 # Get sale details
GET  /api/sales/reports/daily        # Daily sales report
GET  /api/sales/reports/monthly      # Monthly sales report
```

### Customers
```python
GET    /api/customers                # Get all customers
POST   /api/customers                # Add new customer
GET    /api/customers/<id>           # Get customer details
PUT    /api/customers/<id>           # Update customer
DELETE /api/customers/<id>           # Delete customer
```

## Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_models.py

# Run with verbose output
pytest -v
```

## Database Initialization

Create a script `init_db.py` to set up the database:

```bash
python init_db.py
```

## Sample Usage

```python
# Example: Add a new medication
from app.models import Medication
from app.utils.database import db

medication = Medication(
    name="Paracetamol 500mg",
    generic_name="Acetaminophen",
    category="Analgesic",
    manufacturer="PharmaCorp",
    unit_price=2.50,
    quantity_in_stock=500,
    reorder_level=100,
    prescription_required=False
)
db.session.add(medication)
db.session.commit()

# Example: Process a sale
from app.controllers.sales_controller import process_sale

sale_data = {
    'customer_id': 1,
    'items': [
        {'medication_id': 1, 'quantity': 2},
        {'medication_id': 5, 'quantity': 1}
    ],
    'payment_method': 'cash'
}
sale = process_sale(sale_data)
```

## Security Considerations

- Passwords hashed using Werkzeug security (PBKDF2)
- SQL injection prevention via parameterized queries (SQLAlchemy ORM)
- Input validation and sanitization
- CSRF protection (Flask-WTF)
- Session management and timeouts
- Role-based access control (RBAC)
- Secure password policies
- HTTPS encryption in production

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style
- Follow PEP 8 guidelines
- Use Black for code formatting
- Run flake8 for linting
- Write docstrings for all functions and classes
- Add type hints where appropriate

## Deployment

### Production Checklist
- [ ] Set `DEBUG=False` in production
- [ ] Use strong `SECRET_KEY`
- [ ] Configure proper database credentials
- [ ] Set up SSL/TLS certificates
- [ ] Configure firewall rules
- [ ] Set up regular database backups
- [ ] Enable logging and monitoring
- [ ] Use a production WSGI server (Gunicorn/uWSGI)

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker Deployment
```bash
docker build -t pharmacy-management .
docker run -p 5000:5000 pharmacy-management
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Compliance

**Important**: This system handles sensitive medical data. Ensure compliance with:
- HIPAA (Health Insurance Portability and Accountability Act)
- Local pharmacy regulations
- Data protection laws (GDPR, CCPA, etc.)
- Medical record retention requirements
- Prescription drug monitoring programs (PDMP)

## Support

For support and questions:
- Create an issue in the GitHub repository
- Email: support@pharmacy-mgmt.com
- Documentation: Check the `/docs` folder

## Roadmap

- [ ] Web-based interface using Flask templates
- [ ] Mobile app integration (API ready)
- [ ] AI-powered inventory forecasting
- [ ] Advanced analytics dashboard with Plotly
- [ ] Automated supplier ordering
- [ ] SMS notifications for prescription refills
- [ ] Integration with insurance verification systems
- [ ] Multi-pharmacy chain support

## Authors

- Your Name - Initial work

## Acknowledgments

- Flask/Django community
- SQLAlchemy documentation
- Python packaging community
