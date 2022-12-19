# тестируй на 10^8

import numpy as np
from numba import njit


@njit(fastmath=True)
def test_function(x, y):
    return np.sin(np.pi * x) * np.cos(np.pi * y / 2)


def monte_carlo_integration_1(func, dimensions, frequency=1000000, rng=None):
    """
        Функция возвращает значение повторного интеграла функции func арности
        dimensions в единичном кубе [0,1] размерности dimensions. Вычисление
        происходит методом Монте-Карло. Количество случайных величин для каждой
        переменной задается параметром frequency.
    """
    _MAX_BLOCK_SIZE = 10000000
    if not rng:
        rng = np.random.default_rng()
    blocks_number = frequency // _MAX_BLOCK_SIZE + 1 \
        if frequency % _MAX_BLOCK_SIZE != 0 else frequency // _MAX_BLOCK_SIZE
    block_size = int(np.ceil(frequency / blocks_number))
    block_sums = np.zeros(blocks_number)
    random_floats = np.zeros((dimensions, block_size))
    for i in np.arange(blocks_number):
        for j in np.arange(dimensions):
            random_floats[j] = rng.random(block_size)
        block_sums[i] = np.sum(func(*random_floats))
    return np.sum(block_sums) / frequency


def monte_carlo_integration_2(func, dimensions, frequency=1000000, rng=None):
    """
        Функция возвращает значение повторного интеграла функции func арности
        dimensions в единичном кубе [0,1] размерности dimensions. Вычисление
        происходит методом Монте-Карло. Количество случайных величин для каждой
        переменной задается параметром frequency.
    """
    _MAX_BLOCK_SIZE = 10000000
    if not rng:
        rng = np.random.default_rng()
    blocks_number = frequency // _MAX_BLOCK_SIZE + 1 \
        if frequency % _MAX_BLOCK_SIZE != 0 else frequency // _MAX_BLOCK_SIZE
    block_size = int(np.ceil(frequency / blocks_number))
    block_counters = np.zeros(blocks_number)
    random_floats = np.zeros((dimensions, block_size))
    for i in np.arange(blocks_number):
        for j in np.arange(dimensions):
            random_floats[j] = rng.random(block_size)
        level = rng.random(block_size)
        block_counters[i] = np.count_nonzero(func(*random_floats) >= level)
    return np.sum(block_counters) / frequency


def main():
    n = int(input('Введите количество значений случайной величины: '))
    print('Метод 1:', monte_carlo_integration_1(test_function, 2, frequency=n))
    print('Метод 2:', monte_carlo_integration_2(test_function, 2, frequency=n))
    print('Ожидаемый результат:', 4 / (np.pi * np.pi))


if __name__ == '__main__':
    main()
