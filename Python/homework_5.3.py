import sqlite3

connection = sqlite3.connect('3.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    price_per_unit REAL NOT NULL,
    supplier_id INTEGER NOT NULL
);
''')

cursor.execute("INSERT INTO products (product_name, price_per_unit, supplier_id) VALUES ('Product A', 5.5, 1)")
cursor.execute("INSERT INTO products (product_name, price_per_unit, supplier_id) VALUES ('Product B', 3.2, 1)")
cursor.execute("INSERT INTO products (product_name, price_per_unit, supplier_id) VALUES ('Product C', 7.8, 3)")
cursor.execute("INSERT INTO products (product_name, price_per_unit, supplier_id) VALUES ('Product D', 4.1, 5)")
cursor.execute("INSERT INTO products (product_name, price_per_unit, supplier_id) VALUES ('Product E', 6.0, 3)")
cursor.execute("INSERT INTO products (product_name, price_per_unit, supplier_id) VALUES ('Product F', 8.0, 1)")
cursor.execute("INSERT INTO products (product_name, price_per_unit, supplier_id) VALUES ('Product G', 3.9, 5)")

connection.commit()

query = """
SELECT supplier_id, MAX(price_per_unit) AS max_price
FROM products
WHERE supplier_id IN (1, 3, 5)
GROUP BY supplier_id
ORDER BY supplier_id;
"""
cursor.execute(query)

result = cursor.fetchall()

for row in result:
    print(f"ID поставщика: {row[0]}, Максимальная цена: {row[1]}")

connection.close()
