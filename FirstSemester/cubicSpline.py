import numpy as np
import matplotlib.pyplot as plt
from tridiagonalMatrixAlgorithm import tridiagonal_matrix_algorithm


def safe_float(s: str) -> float | None:
    try:
        return float(s)
    except ValueError:
        return None


DEMO_NAME = ('sin(x)', 'x^3', '|x|^3')
DEMO_FUNCTION = (np.sin, lambda x: x ** 3, lambda x: abs(x) ** 3)

TARGET_POINTS = (
    np.arange(0, 2 * np.pi, 1),  # demo 1
    [2, 3, 5, 6],                # demo 2
    [-2, -1, 0, 1, 2]            # demo 3
)

TARGET_VALUES = [[DEMO_FUNCTION[i](TARGET_POINTS[i][j])
                  for j in range(len(TARGET_POINTS[i]))]
                 for i in range(len(DEMO_FUNCTION))]

TARGET_BOUNDARY_CONDITIONS = (
    ((1, 0, 1), (0, 1, 1)),     # demo 1
    ((1, 1, 24), (1, 1, 144)),  # demo 2
    ((1, 1, 0), (1, 1, 24))    # demo 3
)


class CubeSpline:
    def __init__(self, points, values,
                 boundary_condition1, boundary_condition2):
        self._points = np.array(points)
        self._values = np.array(values)
        # вычисляем коэффициенты (lower, main, upper, terms) уравнений во
        # внутренних точках
        n = len(points) - 1
        points_diffs = np.array([points[i] - points[i - 1]
                                 for i in np.arange(1, n + 1)])
        lower = np.zeros(n)
        lower[:n - 1] = points_diffs[:n - 1] / 6
        main = np.zeros(n + 1)
        main[1:n] = (points_diffs[:n - 1] + points_diffs[1:n]) / 3
        upper = np.zeros(n)
        upper[1:] = points_diffs[1:n] / 6
        values_diffs = np.array([values[i] - values[i - 1]
                                 for i in np.arange(1, n + 1)])
        terms = np.zeros(n + 1)
        terms[1:n] = (values_diffs[1:n] / points_diffs[1:n] -
                      values_diffs[:n - 1] / points_diffs[:n - 1])
        # вычисляем коэффициенты (lower, main, upper, terms) уравнений на
        # границах
        alpha0, beta0, gamma0 = boundary_condition1
        main[0] = -alpha0 * points_diffs[0] / 3 + beta0
        upper[0] = -alpha0 * points_diffs[0] / 6
        terms[0] = gamma0 - values_diffs[0] / points_diffs[0] * alpha0

        alpha1, beta1, gamma1 = boundary_condition2
        lower[-1] = alpha1 * points_diffs[-1] / 6
        main[-1] = alpha1 * points_diffs[-1] / 3 + beta1
        terms[-1] = gamma1 - values_diffs[-1] / points_diffs[-1] * alpha1
        # вычисляем коэффициенты сплайна на интервалах
        self._coefficients = tridiagonal_matrix_algorithm(upper, main,
                                                          lower, terms)

    def calculate(self, point):
        n = len(self._points) - 1
        # поиск интервала
        interval_start = 0
        for i in np.arange(n):
            if point <= self._points[i + 1]:
                interval_start = i
                break
        if point >= self._points[-1]:
            interval_start = n - 1
        # подготовка к вычислению сплайна на найденном интервале
        points_diff = (self._points[interval_start + 1] -
                       self._points[interval_start])
        point_i_minus_point = self._points[interval_start + 1] - point
        point_minus_point_i_minus_1 = point - self._points[interval_start]
        return (  # вычисление сплайна
            (  # 1-е слагаемое
                self._coefficients[interval_start] *
                point_i_minus_point ** 3 / (6 * points_diff)
            ) + (  # 2-е
                self._coefficients[interval_start + 1] *
                point_minus_point_i_minus_1 ** 3 / (6 * points_diff)
            ) + (  # 3-е
                (self._values[interval_start] -
                 self._coefficients[interval_start] *
                 points_diff ** 2 / 6) *
                point_i_minus_point / points_diff
            ) + (  # 4-е
                (self._values[interval_start + 1] -
                 self._coefficients[interval_start + 1] *
                 points_diff ** 2 / 6) *
                point_minus_point_i_minus_1 / points_diff
            )
        )

    def show(self, point=None, frequency=10e-5,
             title='spline', xlabel='x', ylabel='y', grid=False):
        # подготовка данных для графика
        start, end = self._points[0], self._points[-1]
        if point is not None:
            start, end = min(start, point), max(end, point)
        points = np.arange(start, end, frequency)
        values = np.array([*map(lambda p: self.calculate(p), points)])
        # описание графика
        plt.plot(points, values, 'g', self._points, self._values, 'ro')
        if point is not None:
            plt.plot(point, self.calculate(point), 'bx')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xlim(xmin=start - 0.15, xmax=end + 0.15)
        plt.grid(grid)
        # вывод графика
        plt.show()


def main():
    for i in range(len(DEMO_FUNCTION)):
        print(f'Демо {i + 1}:', DEMO_NAME[i])
        demo_spline = CubeSpline(TARGET_POINTS[i], TARGET_VALUES[i],
                                 TARGET_BOUNDARY_CONDITIONS[i][0],
                                 TARGET_BOUNDARY_CONDITIONS[i][1])
        interpolation_point = safe_float(input('Введите точку интерполяции: '))
        demo_spline.show(interpolation_point)
        if interpolation_point is not None:
            spline_value = demo_spline.calculate(interpolation_point)
            function_value = DEMO_FUNCTION[i](interpolation_point)
            print('Значение сплайна в точке интерполяции:', spline_value)
            print('Значение интерполируемой функции в точке интерполяции:',
                  function_value)
            print('Абсолютная точность:', abs(function_value - spline_value))


if __name__ == '__main__':
    main()
