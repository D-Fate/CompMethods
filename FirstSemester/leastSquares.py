import numpy as np
import matplotlib.pyplot as plt


# X = np.array([-8, -4, 0, 1, 2, 3])
# Y = np.array([-5, -3, 0, 2, 1, 3])

X = np.arange(-np.pi / 2, np.pi / 2, np.pi / 31)
Y = [np.cos(p) for p in X]

M = 5

N = len(X)
# M = 2

FREQUENCY = 31


def calculate_polynom(coefficients: np.array, point: float) -> float:
    result = 0
    for i in np.arange(len(coefficients)):
        result += coefficients[i] * point ** i
    return result


def main():
    f = np.zeros(M)
    for i in np.arange(M):
        s = 0
        for j in np.arange(N):
            s += Y[j] * X[j] ** i
        f[i] = s

    g = np.zeros(shape=(M, M))
    for i in np.arange(M):
        for j in np.arange(M):
            s = 0
            for k in np.arange(N):
                s += X[k] ** (i + j)
            g[i, j] = s

    print('Матрица Грама:')
    print(*g, sep='\n')

    print()

    a = np.linalg.inv(g).dot(f)

    print('Коэффициенты найденного многочлена:')
    print(a)

    polynom_points = np.arange(-10, 10, FREQUENCY)
    polynom_values = np.array(
        [*map(lambda p: calculate_polynom(a, p), polynom_points)]
    )

    plt.plot(polynom_points, polynom_values, 'g', X, Y, 'rx')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(xmin=-np.pi / 2, xmax=np.pi / 2)
    plt.ylim(ymin=-0.1, ymax=1.25)
    plt.show()


if __name__ == '__main__':
    main()
