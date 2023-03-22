import numpy as np


INITIAL_APPROXIMATION = (0, 1)


def target_function(x, y):
    return x**2 + y**2


def gradient_descent(func, matrix: np.array, init_approximation: np.array,
                     precision=10e-6) -> np.array:
    x = init_approximation
    omega = matrix.dot(init_approximation) - func(*init_approximation)
    y = matrix.dot(omega)
    r = omega.dot(omega)
    s = y.dot(omega)
    while s >= precision ** 2:
        t = r / s
        x -= t * omega
        omega -= t * y
        r = omega.dot(omega)
        s = y.dot(omega)
    return x


def main():
    pass


if __name__ == '__main__':
    main()