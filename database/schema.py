def get_schema():
    return """
Table customers(
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
)

Table orders(
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    total_amount NUMERIC(10,2),
    order_date TIMESTAMP
)

Table products(
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    category VARCHAR(100),
    price NUMERIC(10,2),
    stock INTEGER,
    created_at TIMESTAMP
)

Table payments(
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    payment_method VARCHAR(50),
    amount NUMERIC(10,2),
    status VARCHAR(50),
    payment_date DATE
)
"""
