import numpy as np
import matplotlib.pyplot as plt


X = np.array([-8, -4, 0, 1, 2, 3])
Y = np.array([-5, -3, 0, 2, 1, 3])

N = len(X)
M = 2

FREQUENCY = 10e-5


def calculate_polynom(coefficients: np.array, point: np.float64):
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

    print('Матрица G:')
    print(*g, sep='\n')

    print()

    a = np.linalg.inv(g).dot(f)
    print('Столбец A:')
    print(a)

    polynom_points = np.arange(-10, 10, FREQUENCY)
    polynom_values = np.array(
        [*map(lambda p: calculate_polynom(a, p), polynom_points)]
    )

    plt.plot(polynom_points, polynom_values, 'g', X, Y, 'rx')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(xmin=-10, xmax=10)
    plt.ylim(ymin=-10, ymax=10)
    plt.show()


if __name__ == '__main__':
    main()
