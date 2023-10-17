import numpy as np
import matplotlib.pyplot as plt
from simpson import composite_simpson_rule


N = 5

A, B = -np.pi / 2, np.pi / 2
TARGET_FUNCTION = np.cos

FREQUENCY = 10e-5


def calculate_polynom(coefficients: np.array, point: float) -> float:
    result = 0
    for i in np.arange(len(coefficients)):
        result += coefficients[i] * point ** i
    return result


def main():
    g = np.zeros(shape=(N, N))
    for i in np.arange(N):
        for j in np.arange(N):
            g[i][j], _ = composite_simpson_rule(lambda x: x**(i + j), A, B)

    print('Матрица Грама:')
    print(*g, sep='\n')

    print()

    f = np.zeros(N)
    for i in np.arange(N):
        f[i], _ = composite_simpson_rule(
            lambda x: TARGET_FUNCTION(x) * x**i, A, B
        )

    a = np.linalg.inv(g).dot(f)
    print('Коэффициенты найденного многочлена:')
    print(a)

    polynom_points = np.arange(A, B, FREQUENCY)
    polynom_values = np.array(
        [*map(lambda p: calculate_polynom(a, p), polynom_points)]
    )
    func_values = np.array(
        [*map(lambda p: TARGET_FUNCTION(p), polynom_points)]
    )

    plt.figure(1)
    plt.plot(polynom_points, polynom_values, 'g')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(xmin=A, xmax=B)
    plt.ylim(ymin=0, ymax=1.25)
    plt.title('Polynomial')

    plt.figure(2)
    plt.plot(polynom_points, func_values, 'r')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(xmin=A, xmax=B)
    plt.ylim(ymin=0, ymax=1.25)
    plt.title('cos')

    plt.figure(3)
    plt.plot(polynom_points, func_values - polynom_values, 'r')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(xmin=A, xmax=B)
    plt.ylim(ymin=0, ymax=1.25)
    plt.title('cos - p')

    plt.show()


if __name__ == '__main__':
    main()
