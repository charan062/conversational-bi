import sqlite3

conn = sqlite3.connect("data/sales.db")
cursor = conn.cursor()

# Insert customers
customers = [
    (1, "Customer A", "India", "2023-01-10", "SMB"),
    (2, "Customer B", "USA", "2023-02-15", "Enterprise"),
    (3, "Customer C", "UK", "2023-03-20", "Startup")
]

cursor.executemany(
    "INSERT INTO customers VALUES (?, ?, ?, ?, ?)",
    customers
)

# Insert products
products = [
    (1, "Product X", "Software", 100.0, 60.0),
    (2, "Product Y", "Hardware", 200.0, 120.0)
]

cursor.executemany(
    "INSERT INTO products VALUES (?, ?, ?, ?, ?)",
    products
)

# Insert orders
orders = [
    (1, 1, 1, "2024-01-01", 2, 200.0),
    (2, 2, 2, "2024-01-05", 1, 200.0),
    (3, 1, 2, "2024-02-01", 1, 200.0)
]

cursor.executemany(
    "INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)",
    orders
)

conn.commit()
conn.close()

print("Sample data inserted")
