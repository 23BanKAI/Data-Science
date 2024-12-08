import datetime

class Product:
    def __init__(self, name, quantity, price):
        self.name = name
        self.quantity = quantity
        self.price = price

    def increase_quantity(self, amount):
        self.quantity += amount
        print(f"Количество товара '{self.name}' увеличено на {amount}. Сейчас на складе {self.quantity} единиц.")

    def decrease_quantity(self, amount):
        if amount <= self.quantity:
            self.quantity -= amount
            print(f"Количество товара '{self.name}' уменьшено на {amount}. Осталось на складе {self.quantity} единиц.")
        else:
            print(f"Ошибка: недостаточно товара '{self.name}' на складе для продажи.")

    def total_cost(self):
        return self.quantity * self.price


class Warehouse:
    def __init__(self):
        self.products = []
        self.history = []

    def add_product(self, product):
        self.products.append(product)
        self.log_operation(f"Товар '{product.name}' добавлен на склад.")

    def remove_product(self, product_name):
        for product in self.products:
            if product.name == product_name:
                self.products.remove(product)
                self.log_operation(f"Товар '{product_name}' удалён со склада.")
                break
        else:
            print(f"Ошибка: товар '{product_name}' не найден на складе.")

    def log_operation(self, operation):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append(f"{timestamp} - {operation}")

    def total_value(self):
        return sum(product.total_cost() for product in self.products)


class Seller:
    def __init__(self, name):
        self.name = name
        self.sales = []

    def sell_product(self, product, amount):
        product.decrease_quantity(amount)
        sale_value = amount * product.price
        self.sales.append((product.name, amount, sale_value))
        print(f"Продано {amount} единиц товара '{product.name}' на сумму {sale_value}.")

    def report_sales(self):
        print(f"Отчёт о продажах продавца {self.name}:")
        for sale in self.sales:
            print(f"Товар: {sale[0]}, Количество: {sale[1]}, Сумма: {sale[2]}")


if __name__ == "__main__":
    product1 = Product("Ноутбук", 10, 50000)
    product2 = Product("Телефон", 20, 15000)

    warehouse = Warehouse()

    warehouse.add_product(product1)
    warehouse.add_product(product2)

    seller = Seller("Иван")

    seller.sell_product(product1, 3)
    seller.sell_product(product2, 5)

    seller.report_sales()

    print(f"\nОбщая стоимость товаров на складе: {warehouse.total_value()}")

    print("\nИстория операций на складе:")
    for log in warehouse.history:
        print(log)
