from math_tools.calculator import Calculator

def main():
    numbers = [1, 2.5, 3, 4.5, 5]
    calculator = Calculator()
    result = calculator.sum_list(numbers)
    print(f"Сумма чисел {numbers}: {result}")

if __name__ == "__main__":
    main()