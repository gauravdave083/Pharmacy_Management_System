// MongoDB initialization script
db = db.getSiblingDB('pharmacy_management');

// Create collections with validation
db.createCollection('medications', {
    validator: {
        $jsonSchema: {
            bsonType: 'object',
            required: ['name', 'price', 'stock_quantity'],
            properties: {
                name: { bsonType: 'string' },
                price: { bsonType: 'number', minimum: 0 },
                stock_quantity: { bsonType: 'int', minimum: 0 }
            }
        }
    }
});

db.createCollection('customers');
db.createCollection('sales');
db.createCollection('prescriptions');
db.createCollection('suppliers');
db.createCollection('users');

print('Database initialized successfully');