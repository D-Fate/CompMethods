from typing import Tuple
from math import sin


def secant(f, start, end, precision=0.00001) -> Tuple[float, int]:
    """
        Функция возвращает решение уравнения f(x) = 0 на заданном интервале с
        точностью, равной precision, полученное методом секущих.
        Предполагается, что корень уже отделён на заданном интервале.
    """
    previous = start
    current = end
    next = current - (current - previous) / \
        (f(current) - f(previous)) * f(current)
    iterations = 1
    while abs(f(next)) >= precision:
        previous = current
        current = next
        next = current - (current - previous) / \
            (f(current) - f(previous)) * f(current)
        iterations += 1
    return next, iterations


if __name__ == '__main__':
    print('Корень = {0}, кол-во итераций = {1}'.format(*secant(sin, 3, 4)))
