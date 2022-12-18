import numpy as np


TARGET_MATRIX = [
    [1, 2, 0, 0, 0],
    [4, 5, 6, 0, 0],
    [0, 7, 8, 9, 0],
    [0, 0, 10, 11, 12],
    [0, 0, 0, 13, 14]
]

TARGET_UPPER = [TARGET_MATRIX[i][i + 1] for i in range(len(TARGET_MATRIX) - 1)]
TARGET_MAIN = [TARGET_MATRIX[i][i] for i in range(len(TARGET_MATRIX))]
TARGET_LOWER = [TARGET_MATRIX[i][i - 1] for i in range(1, len(TARGET_MATRIX))]
TARGET_TERMS = [sum(row) for row in TARGET_MATRIX]


def tridiagonal_matrix_algorithm(upper, main,
                                 lower, terms) -> np.ndarray | None:
    """
        Функция возвращает решение системы линейных уравнений, заданной
        тридиагональной матрицей. Если матрица вырождена, то результат — None.
    """
    rank = len(terms)
    p = np.zeros(rank - 1, float)
    q = np.zeros(rank, float)

    # инициализация начальных прогоночных коэффициентов
    if main[0] == 0:
        return None
    p[0] = upper[0] / main[0]
    q[0] = terms[0] / main[0]

    # вычисление прогоночных коэффициентов
    for i in np.arange(1, rank - 1):
        denominator = main[i] - lower[i - 1] * p[i - 1]
        if denominator == 0:
            return None
        p[i] = upper[i] / denominator
        q[i] = (terms[i] - lower[i - 1] * q[i - 1]) / denominator

    # вычисление прогоночных коэффициентов (i = rank - 1)
    denominator = main[rank - 1] - lower[rank - 2] * p[rank - 2]
    if denominator == 0:
        return None
    q[rank - 1] = (
            (terms[rank - 1] - lower[rank - 2] * q[rank - 2]) / denominator
    )
    # вычисление решения
    result = np.zeros(rank, float)
    result[rank - 1] = q[rank - 1]
    for i in np.arange(rank - 1, 0, -1):
        result[i - 1] = q[i - 1] - p[i - 1] * result[i]
    return result


if __name__ == '__main__':
    print('Матрица:')
    print(*TARGET_MATRIX, sep='\n', end='\n\n')
    print('Верхняя диагональ:', *TARGET_UPPER)
    print('Главная диагональ:', *TARGET_MAIN)
    print('Нижняя диагональ:', *TARGET_LOWER)
    print('Свободные коэффициенты:', *TARGET_TERMS)
    print()
    print('Решение:', tridiagonal_matrix_algorithm(
        TARGET_UPPER, TARGET_MAIN, TARGET_LOWER, TARGET_TERMS
    ))
