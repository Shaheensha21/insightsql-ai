import sqlite3
import random
from datetime import datetime, timedelta
import os

# Get correct base path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

db_path = os.path.join(BASE_DIR, "sales.db")
schema_path = os.path.join(BASE_DIR, "schema.sql")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create tables
with open(schema_path, "r") as f:
    cursor.executescript(f.read())

# Insert customers
customers = [
    (1, "Amit", "Hyderabad", "2023-01-10"),
    (2, "Priya", "Bangalore", "2023-02-15"),
    (3, "Rahul", "Chennai", "2023-03-20"),
    (4, "Sneha", "Mumbai", "2023-04-12")
]

cursor.executemany("INSERT INTO customers VALUES (?, ?, ?, ?)", customers)

# Insert products
products = [
    (1, "Laptop", "Electronics", 70000),
    (2, "Phone", "Electronics", 25000),
    (3, "Shoes", "Fashion", 3000)
]

cursor.executemany("INSERT INTO products VALUES (?, ?, ?, ?)", products)

# Insert orders
orders = []
for i in range(1, 21):
    customer_id = random.randint(1, 4)
    product_id = random.randint(1, 3)
    date = datetime.now() - timedelta(days=random.randint(1, 120))
    quantity = random.randint(1, 3)
    price_map = {1:70000, 2:25000, 3:3000}
    total_amount = quantity * price_map[product_id]
    orders.append((i, customer_id, product_id, date.strftime("%Y-%m-%d"), quantity, total_amount))

cursor.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)", orders)

conn.commit()
conn.close()

print("✅ Database created and seeded successfully.")
