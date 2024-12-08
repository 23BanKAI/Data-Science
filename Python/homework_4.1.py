from datetime import datetime

current_datetime = datetime.now()
print(f"Текущая дата и время: {current_datetime}")

date1 = datetime(2024, 12, 8)
date2 = datetime(2023, 12, 8)

date_difference = date1 - date2
print(f"Разница между {date1} и {date2} составляет {date_difference.days} дней.")

date_string = "2024-12-08 14:30:00"
date_object = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
print(f"Преобразованная дата и время: {date_object}")

