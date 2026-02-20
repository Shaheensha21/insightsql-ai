SCHEMA_DESCRIPTION = """
Tables:

customers(id, name, city, signup_date)
products(id, name, category, price)
orders(id, customer_id, product_id, order_date, quantity, total_amount)

Relationships:
orders.customer_id references customers.id
orders.product_id references products.id
"""
