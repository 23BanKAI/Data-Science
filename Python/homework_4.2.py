import itertools

def infinite_numbers(start=0):
    return itertools.count(start)

print("Первые 10 чисел:")
for i, num in enumerate(infinite_numbers(5)):
    if i >= 10:
        break
    print(num, end=" ")

print("\n")

def square(x):
    return x ** 2

numbers = [1, 2, 3, 4, 5]
squared_numbers = map(square, numbers)

print("Квадраты чисел:")
for num in squared_numbers:
    print(num, end=" ")

print("\n")

list1 = [1, 2, 3]
list2 = ['a', 'b', 'c']
list3 = [True, False]

combined = itertools.chain(list1, list2, list3)

print("Объединенные элементы из нескольких итераторов:")
for item in combined:
    print(item, end=" ")

print("\n")

try:
    empty_iter = iter([])
    first_element = next(empty_iter)
except StopIteration:
    print("Ошибка: итератор пуст!")
