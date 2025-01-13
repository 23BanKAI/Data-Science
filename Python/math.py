import numpy as np

A = np.array([
    [3, 3, -4, -3],
    [0, 6, 1, 1],
    [5, 4, 2, 1],
    [2, 3, 3, 2]
])

# Вычисление обратной матрицы
A_inv = np.linalg.inv(A)

# Нахождение наибольшего элемента в обратной матрице
max_element = np.max(A_inv)
print(max_element)

