import sqlite3

connection = sqlite3.connect('example.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    price_per_unit REAL NOT NULL
);
''')

cursor.execute("INSERT INTO products (product_name, price_per_unit) VALUES ('Product 1', 5.5)")
cursor.execute("INSERT INTO products (product_name, price_per_unit) VALUES ('Product 2', 3.0)")
cursor.execute("INSERT INTO products (product_name, price_per_unit) VALUES ('Product 3', 6.9)")
cursor.execute("INSERT INTO products (product_name, price_per_unit) VALUES ('Product 4', 2.5)")
cursor.execute("INSERT INTO products (product_name, price_per_unit) VALUES ('Product 5', 7.5)")

connection.commit()

cursor.execute("SELECT product_name FROM products WHERE price_per_unit >= 3 AND price_per_unit < 7")
product_names = cursor.fetchall()

for product in product_names:
    print(product[0])

connection.close()
