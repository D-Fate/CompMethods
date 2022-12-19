from typing import Tuple
from math import sin


def dichotomy(f, start, end, precision=0.00001) -> Tuple[None | float, int]:
    """
        Функция возвращает решение уравнения f(x) = 0 на заданном интервале с
        точностью, равной precision, полученное методом дихотомии.
        Предполагается, что корень уже отделён на заданном интервале.
        При некорректных данных функция вернёт None.
    """
    a = f(start)
    b = f(end)
    iterations = 0
    if a * b < 0:
        while True:
            center = (start + end) / 2
            c = f(center)
            if a * c <= 0:
                end = center
                b = c
            else:
                start = center
                a = c
            iterations += 1
            if abs(end - start) < precision:
                return (start + end) / 2, iterations
    return None, iterations


def main():
    print('Корень = {0}, кол-во итераций = {1}'.format(*dichotomy(sin, 3, 4)))


if __name__ == '__main__':
    main()