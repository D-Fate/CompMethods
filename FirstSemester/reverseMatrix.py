import numpy as np


TARGET_MATRIX = np.array([
    [0.2, 0.5, 0.7],
    [0.6, 0.3, 0.4],
    [0.5, -0.2, -0.3]
])


def similarity_measure(matrix1: np.ndarray, matrix2: np.ndarray) -> np.ndarray:
    """ Функция возвращает показатель близости матриц matrix1 и matrix2. """
    return np.sum(np.abs((matrix1 - matrix2)))


def reverse(matrix: np.ndarray, precision=10e-9) -> np.ndarray | None:
    """
        Функция возвращает матрицу, обратную матрице matrix. Обратная
        матрица находится с заданной точностью precision. В случае ошибки
        функция возвращает None.
    """
    rank = len(matrix)
    m = np.hstack((matrix, np.identity(rank)))
    # прямой ход
    for i in np.arange(rank):
        # поиск опорного элемента
        pivot = np.abs(m[i, i])
        pivot_i = i
        for j in np.arange(i + 1, rank):
            if np.abs(m[j, i]) > pivot:
                pivot = np.abs(m[j, i])
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
        for j in np.arange(i + 1, rank):
            m[j, :] -= m[i, :] * m[j, i]
    # обратный ход
    for i in np.arange(rank - 1, 0, -1):
        for j in np.arange(i - 1, -1, -1):
            if m[j, i]:
                m[j, :] -= m[i, :] * m[j, i]
    return m[:, rank:]


def refine_reverse(matrix: np.ndarray,
                   reverse_approximation: np.ndarray) -> np.ndarray | None:
    """
        Функция уточняет приближение матрицы, обратной к matrix, заданное
        reverse_approximation.
    """
    rank = len(matrix)
    identity = np.identity(rank)
    reverse_matrix = reverse_approximation
    print()
    for i in np.arange(5):
        print(f'Показатель близости, шаг {i}:',
              similarity_measure(matrix.dot(reverse_matrix), identity))
        reverse_matrix = reverse_matrix.dot(
            2 * identity - matrix.dot(reverse_matrix)
        )
    return reverse_matrix


def main():
    rank = len(TARGET_MATRIX)
    identity = np.identity(rank)

    print('Тестовая матрица:', *TARGET_MATRIX, sep='\n')

    reverse_matrix = reverse(TARGET_MATRIX)

    if reverse_matrix is None:
        print('\nМатрица вырождена.')
        return

    print('\nОбратная матрица:', *reverse_matrix, sep='\n')
    print('\nПоказатель близости:', similarity_measure(
        TARGET_MATRIX.dot(reverse_matrix), identity
    ))

    print()

    rng = np.random.default_rng()
    corruption = \
        0.01 * abs(int(input('Введите процент искажения обратной матрицы\n> ')))

    corrupted_matrix = reverse_matrix.dot(
        np.diag(rng.uniform(high=1 + corruption, low=1 - corruption, size=rank))
    )

    print('\nИскаженная обратная матрица:', *corrupted_matrix, sep='\n')

    refined_reverse_matrix = refine_reverse(TARGET_MATRIX, corrupted_matrix)
    if similarity_measure(reverse_matrix, refined_reverse_matrix) > 1:
        print('\nИтерационный процесс расходится. '
              'Обратная матрица не может быть приближена.')
        return

    print('\nВосстановленная обратная матрица:',
          *refined_reverse_matrix, sep='\n')
    print('\nПоказатель близости:', similarity_measure(
        TARGET_MATRIX.dot(refined_reverse_matrix), identity
    ))


if __name__ == '__main__':
    main()
