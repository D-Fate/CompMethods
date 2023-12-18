import numpy as np


def f(x, y):
    return y + x * np.exp(x)


def exact_solution(x, x0, y0):
    c = np.exp(-x0) * (y0 - 1/2 * x0 ** 2)
    return np.exp(x) * (1/2 * x ** 2 + c)


def _step(x, y, h, func):
    phi0 = h * func(x, y)
    phi1 = h * func(x + h / 2, y + phi0 / 2)
    phi2 = h * func(x + h / 2, y + phi1 / 2)
    phi3 = h * func(x + h, y + phi2)
    return y + (phi0 + 2 * phi1 + 2 * phi2 + phi3) / 6


def _jump(x, y, h, func, precision):
    current_step = _step(x, y, h, func)
    while True:
        half_step = _step(x, y, h / 2, func)
        next_step = _step(x + h / 2, half_step, h / 2, func)
        if np.abs(current_step - next_step) < precision:
            return x + h, current_step, h
        h /= 2
        current_step = half_step


def solve_cauchy(x, y, h, end, func, precision=10e-5):
    while x < end:
        x, y, _ = _jump(x, y, h, func, precision)
        if end - x < h:
            h = end - x
    return x, y


def main():
    x0, end = map(
        float,
        input('Введите левую и правую границы отрезка (x0, X)\n>> ').split()
    )
    y0, h = map(
        float,
        input('Введите начальное значение y0 и шаг h0 через пробел\n>> ').split()
    )
    precision = float(input('Введите точность\n>> '))
    x, y = solve_cauchy(x0, y0, h, end, f, precision)
    print(f'Значение узла: {x}\n'
          f'Приближенное решение: {y}\n'
          f'Погрешность: {np.abs(y - exact_solution(end, x0, y0))}')


if __name__ == '__main__':
    main()
