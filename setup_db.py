import sqlite3

# Connect to database
conn = sqlite3.connect("data/sales.db")
cursor = conn.cursor()

# Create customers table
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    country TEXT,
    signup_date TEXT,
    segment TEXT
)
""")

# Create products table
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    name TEXT,
    category TEXT,
    price REAL,
    cost REAL
)
""")

# Create orders table
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER,
    order_date TEXT,
    quantity INTEGER,
    total_amount REAL
)
""")

conn.commit()
conn.close()

print("Database and tables created successfully")
