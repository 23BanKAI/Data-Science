def read_and_print_numbers_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.readlines()
        
        for line in data:
            line = line.strip()
            try:
                # Проверка, является ли строка числом
                if line.isdigit() or (line.replace('.', '', 1).isdigit() and line.count('.') < 2):
                    print(line)
                else:
                    raise TypeError(f"Невозможно преобразовать строку в число: {line}")
            except TypeError as e:
                print(f"Ошибка: {e}")
    
    except FileNotFoundError:
        print(f"Ошибка: файл '{file_path}' не найден.")

file_path = '../Data-Science/Data-Science/Python/data.txt'
read_and_print_numbers_from_file(file_path)
