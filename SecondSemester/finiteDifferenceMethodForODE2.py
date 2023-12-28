import numpy as np


P, Q = 3, -4
A, B = 0, 1
N = 10

TARGET_FUNCTIONS_NAMES = ('x^2', 'sin(x)', 'e^x * x^2')
TARGET_FUNCTIONS = (
    lambda x: x ** 2,
    np.sin,
    lambda x: np.exp(x) * x ** 2
)
TARGET_DERIVATIVES = (
    lambda x: 2 * x,
    np.cos,
    lambda x: np.exp(x) * x ** 2 + 2 * np.exp(x) * x
)
TARGET_SECOND_DERIVATIVES = (
    lambda x: 2,
    lambda x: -np.sin(x),
    lambda x: np.exp(x) * x ** 2 + 4 * np.exp(x) * x + 2 * np.exp(x)
)
TARGET_BOUNDARY_CONDITIONS = [
    ((1, 1, TARGET_FUNCTIONS[i](A) + TARGET_DERIVATIVES[i](A)),
     (1, 1, TARGET_FUNCTIONS[i](B) + TARGET_DERIVATIVES[i](B)))
    for i in range(3)
]


def finite_difference_method(p, q, a, b, n,
                             boundary_conditions, function_with_derivatives):
    assert q < 0
    function = function_with_derivatives[0]
    first_derivative = function_with_derivatives[1]
    second_derivative = function_with_derivatives[2]
    alpha0, beta0, gamma0 = boundary_conditions[0]
    alpha1, beta1, gamma1 = boundary_conditions[1]
    step = (b - a) / n
    points = [a + step * i for i in range(n + 1)]
    values = [function(point) for point in points]
    values[0] = gamma0
    values[n] = gamma1

    diff_op = [0] * (n + 1)
    diff_op[0] = gamma0
    for i in range(1, n):
        diff_op[i] = (second_derivative(points[i]) +
                      p * first_derivative(points[i]) +
                      q * function(points[i])) * step ** 2
    diff_op[n] = gamma1

    lower, main, upper = [0] * (n + 1), [0] * (n + 1), [0] * (n + 1)
    for i in range(n + 1):
        lower[i] = 1 - step * p / 2
        main[i] = -2 + step * step * q
        upper[i] = 1 + step * p / 2
    upper[0] = beta0 / step
    main[0] = alpha0 - beta0 / step
    main[n] = alpha1 + beta1 / step
    lower[n] = -beta1 / step

    u, v = [0] * (n + 1), [0] * (n + 1)
    u[0] = -upper[0] / main[0]
    v[0] = diff_op[0] / main[0]
    for i in range(1, n):
        u[i] = -upper[i] / (lower[i] * u[i - 1] + main[i])
        v[i] = (-lower[i] * v[i - 1] + diff_op[i]) / (lower[i] * u[i - 1] + main[i])
    solution = [0] * (n + 1)
    solution[n] = (-lower[n] * v[n - 1] + diff_op[n]) / (lower[n] * u[n - 1] + main[n])
    for i in reversed(range(n)):
        solution[i] = u[i] * solution[i + 1] + v[i]
    return points, values, solution


def main():
    for i in range(3):
        print(f'Тест {i + 1}: {TARGET_FUNCTIONS_NAMES[i]}')
        function_with_derivatives = (
            TARGET_FUNCTIONS[i],
            TARGET_DERIVATIVES[i],
            TARGET_SECOND_DERIVATIVES[i]
        )
        x, y, solution = finite_difference_method(
            P, Q, A, B, N,
            TARGET_BOUNDARY_CONDITIONS[i],
            function_with_derivatives
        )
        for j in range(N + 1):
            print(f'Узел: {x[j]}\n',
                  f'Ожидаемое значение: {y[j]}\n',
                  f'Полученное значение: {solution[j]}\n',
                  f'Значение погрешности: {abs(y[j] - solution[j])}')
        print()


if __name__ == '__main__':
    main()
