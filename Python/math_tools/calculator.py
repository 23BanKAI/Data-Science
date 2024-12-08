class Calculator:

    @staticmethod
    def sum_list(numbers: list[float]) -> float:
        """
        Вычисляет сумму всех чисел в списке.

        :param numbers: Список чисел.
        :return: Сумма чисел.
        """
        if not all(isinstance(n, (int, float)) for n in numbers):
            raise ValueError("Все элементы списка должны быть числами.")
        return sum(numbers)
