import numpy as np


N = 5
DEMO_MATRIX = np.array([[1 / (i + j + 1) for j in range(N)] for i in range(N)])
DEMO_FUNC_VALUES = np.array([*map(sum, DEMO_MATRIX)])


def demo_function(x, y):
    a, b, c, d = tuple(np.reshape(DEMO_MATRIX, 4))
    f1, f2 = tuple(DEMO_FUNC_VALUES)
    return a * x**2 + (b + c) * x * y + d * y**2 - 2 * (f1 * x + f2 * y)


def gradient_descent(func, matrix: np.array, init_approximation: np.array,
                     precision=10e-6) -> np.array:
    x = init_approximation
    omega = matrix.dot(init_approximation) - func
    while True:
        y = matrix.dot(omega)
        r = omega.dot(omega)
        s = y.dot(omega)
        if s < precision ** 2:
            return x
        t = r / s
        x -= t * omega
        omega -= t * y


def main():
    print('Матрица, ассоциированная с функцией:', *DEMO_MATRIX, sep='\n')
    print('Значения функции:', DEMO_FUNC_VALUES)

    result = gradient_descent(DEMO_FUNC_VALUES, DEMO_MATRIX, np.zeros(N))
    print(result)


if __name__ == '__main__':
    main()