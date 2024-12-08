class DataBuffer:
    def __init__(self):
        self.buffer = []

    def add_data(self, data):
        if len(self.buffer) >= 5:
            print("Переполнение буфера! Очищаю буфер.")
            self.buffer.clear()
        self.buffer.append(data)
        print(f"Данные '{data}' добавлены в буфер.")

    def get_data(self):
        if not self.buffer:
            print("Буфер пуст! Нет данных для получения.")
        else:
            data = self.buffer.pop(0)
            print(f"Данные '{data}' извлечены из буфера.")
            return data


buffer = DataBuffer()
buffer.add_data("data1")
buffer.add_data("data2")
buffer.add_data("data3")
buffer.add_data("data4")
buffer.add_data("data5")
buffer.add_data("data6")
buffer.get_data()
buffer.get_data()
buffer.get_data()
