import sqlite3

connection = sqlite3.connect('2.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    price_per_unit REAL NOT NULL,
    category_id INTEGER NOT NULL
);
''')

cursor.execute("INSERT INTO products (product_name, price_per_unit, category_id) VALUES ('Product A', 5.5, 1)")
cursor.execute("INSERT INTO products (product_name, price_per_unit, category_id) VALUES ('Product B', 3.2, 1)")
cursor.execute("INSERT INTO products (product_name, price_per_unit, category_id) VALUES ('Product C', 7.8, 2)")
cursor.execute("INSERT INTO products (product_name, price_per_unit, category_id) VALUES ('Product D', 4.1, 1)")
cursor.execute("INSERT INTO products (product_name, price_per_unit, category_id) VALUES ('Product E', 6.0, 2)")

connection.commit()

query = """
SELECT MIN(price_per_unit) AS min_price
FROM products
WHERE category_id = 1;
"""
cursor.execute(query)

min_price = cursor.fetchone()

if min_price:
    print(f"Минимальная цена товара в категории 1: {min_price[0]}")
else:
    print("Нет товаров в категории 1.")

connection.close()
