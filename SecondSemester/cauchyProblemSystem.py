import numpy as np
from scipy.linalg import solve


def _target_func(x, u, v) -> np.ndarray:
    return np.array([
        u - v + np.exp(x) * (1 + x * x),
        u + v + np.exp(x) * x
    ])


def _exact_solution(x, x0: float, u0: float, v0: float) -> np.ndarray:
    a = [[np.cos(x0), np.sin(x0)], [np.sin(x0), -np.cos(x0)]]
    b = [[u0 / np.exp(x0) - x0], [v0 / np.exp(x0) - x0 ** 2]]
    c = solve(a, b).flatten()
    return np.array([
        np.exp(x) * (c[0] * np.cos(x) + c[1] * np.sin(x) + x),
        np.exp(x) * (c[0] * np.sin(x) - c[1] * np.cos(x) + x ** 2)
    ])


def _step(x, u, v, h, func) -> np.ndarray:
    phi0, psi0 = h * func(x, u, v)
    phi1, psi1 = h * func(x + h / 2, u + phi0 / 2, v + psi0 / 2)
    phi2, psi2 = h * func(x + h / 2, u + phi1 / 2, v + psi1 / 2)
    phi3, psi3 = h * func(x + h, u + phi2, v + psi2)
    return np.array([
        u + (phi0 + 2 * phi1 + 2 * phi2 + phi3) / 6,
        v + (psi0 + 2 * psi1 + 2 * psi2 + psi3) / 6
    ])


def _jump(x, u, v, h, func, precision):
    current_step = _step(x, u, v, h, func)
    while True:
        half_step = _step(x, u, v, h / 2, func)
        next_step = _step(x + h / 2, half_step[0], half_step[1], h / 2, func)
        if np.abs(current_step[0] - next_step[0]) < precision and \
                np.abs(current_step[1] - next_step[1]) < precision:
            return x + h, current_step[0], current_step[1], h
        h /= 2
        current_step = half_step


def solve_cauchy(x, u, v, h, end, func, precision=10e-5):
    x, u, v, _ = _jump(x, u, v, h, func, precision)
    while x < end:
        if end - x < h:
            h = end - x
        x, u, v, _ = _jump(x, u, v, h, func, precision)
    return x, u, v


def main():
    x0, end = map(
        float,
        input('Введите левую и правую границы отрезка (x0, X)\n>> ').split()
    )
    u0, v0 = map(
        float,
        input('Введите начальные значения u0 и v0 через пробел\n>> ').split()
    )
    h = float(input('Введите шаг h0\n>> '))
    precision = float(input('Введите точность\n>> '))
    x, u, v = solve_cauchy(x0, u0, v0, h, end, _target_func, precision)
    exact_u, exact_v = _exact_solution(x, x0, u0, v0)
    print(f'Значение узла: {x}\n'
          f'Приближенное решение: ({u}, {v})\n'
          f'Погрешность: {(u - exact_u, v - exact_v)}')


if __name__ == '__main__':
    main()
