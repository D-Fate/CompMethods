import numpy as np
from typing import List
from copy import deepcopy
from datetime import datetime


TARGET_MATRIX = [
    [1, 2, 3, 4, 5],
    [1, 2, 3, 4, 4],
    [0, 2, 3, 4, 5],
    [1, 4, 3, 4, 5],
    [2, 4, 5, 8, 10]
]


def vanilla_gauss(matrix: List[List[float]], terms: List[float],
                  error=0.00001) -> List[float] | None:
    """
        Функция возвращает решение системы линейных уравнений, заданной
        матрицей matrix и столбцом свободных коэффициентов terms. Решение
        находится с заданной точностью precision. В случае ошибки
        функция возвращает None.
    """
    _matrix = deepcopy(matrix)
    _terms = deepcopy(terms)
    rank = len(matrix)
    # прямой ход
    i = 0
    while i < rank:
        pivot = abs(_matrix[i][i])
        pivot_i = i
        # поиск опорного элемента в столбце
        for j in range(i + 1, rank):
            if abs(_matrix[j][i]) > pivot:
                pivot = abs(_matrix[j][i])
                pivot_i = j
        # вернуть None, если опорный элемент меньше допустимой точности
        if pivot < error:
            return None
        # перестановка строк
        _matrix[i], _matrix[pivot_i] = _matrix[pivot_i], _matrix[i].copy()
        _terms[i], _terms[pivot_i] = _terms[pivot_i], _terms[i]
        # нормализация уравнений
        for j in range(rank):
            temp = _matrix[j][i]
            # пропускаем нулевой элемент
            if abs(temp) < error:
                continue
            for k in range(rank):
                _matrix[j][k] *= temp ** (-1)
            _terms[j] /= temp
            # не вычитаем уравнение само из себя
            if j == i:
                continue
            for k in range(rank):
                _matrix[j][k] -= _matrix[i][k]
            _terms[j] -= _terms[i]
        i += 1
    # обратный ход
    i = rank - 1
    while i > -1:
        for j in range(rank - 1, -1, -1):
            temp = _matrix[j][i]
            # пропускаем нулевой элемент
            if abs(temp) < error:
                continue
            for k in range(rank):
                _matrix[j][k] *= temp ** (-1)
            _terms[j] /= temp
            # не вычитаем уравнение само из себя
            if j == i:
                continue
            for k in range(rank):
                _matrix[j][k] -= _matrix[i][k]
            _terms[j] -= _terms[i]
        i -= 1
    return _terms


def numpy_gauss(matrix: np.ndarray, terms: np.ndarray,
                precision=0.00001) -> np.ndarray | None:
    """
        Функция возвращает решение системы линейных уравнений, заданной
        матрицей matrix и столбцом свободных коэффициентов terms. Решение
        находится с заданной точностью precision. В случае ошибки
        функция возвращает None.
    """
    m = np.column_stack((matrix, terms))
    rank = len(matrix)
    # прямой ход
    for i in range(rank):
        # поиск опорного элемента
        pivot = abs(m[i, i])
        pivot_i = i
        for j in range(i + 1, rank):
            if abs(m[j, i]) > pivot:
                pivot = abs(m[j, i])
                pivot_i = j
        # вернуть None, если опорный элемент меньше допустимой точности
        if pivot < precision:
            return None
        # перестановка строк
        if pivot_i != i:
            m[i, :], m[pivot_i, :] = m[pivot_i, :], np.copy(m[i, :])
        # нормализация уравнений
        if m[i, i] != 1:
            m[i, :] *= 1 / m[i, i]
        # обнуляем элементы под главной диагональю
        for j in range(i + 1, rank):
            m[j, :] -= m[i, :] * m[j, i]
    # обратный ход
    for i in range(rank - 1, 0, -1):
        for j in range(i - 1, -1, -1):
            if m[j, i]:
                m[j, :] -= m[i, :] * m[j, i]
    return m[:, rank]


if __name__ == '__main__':
    print('Чистый Гаусс.')
    test_matrix = TARGET_MATRIX
    test_terms = [sum(i) for i in test_matrix]
    print('Матрица:', *test_matrix, sep='\n')
    print('Столбец свободных коэффициентов:', test_terms)
    print('Решение:', vanilla_gauss(test_matrix, test_terms))

    print()

    print('NumPy Гаусс.')
    test_matrix = np.array(TARGET_MATRIX, dtype=np.float64)
    test_terms = np.array([sum(i) for i in test_matrix], dtype=np.float64)
    print('Матрица:', *test_matrix, sep='\n')
    print('Столбец свободных коэффициентов:', test_terms)
    print('Решение:', numpy_gauss(test_matrix, test_terms))
