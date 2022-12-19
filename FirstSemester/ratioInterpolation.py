from typing import List
from FirstSemester.gauss import vanilla_gauss


def ratio_interpolation(point: float, points: List[float], values: List[float],
                        numerator_deg: int, denominator_deg: int,
                        gauss_error=0.00001) -> float | None:
    """
        Функция возвращает значение интерполяции в точке point. Дробно-
        рациональная функция задаётся массивами points и values узловых точек и
        значений функции в узловых точках соответственно, а также степенями
        числителя и знаменателя — numerator_deg и
        denominator_deg соответственно.
    """
    deg = numerator_deg + denominator_deg + 1
    matrix: List[List[float]] = [[0.] * deg for _ in range(len(points))]
    for i in range(len(points)):
        matrix[i][0] = 1
        for j in range(1, numerator_deg):
            matrix[i][j] = matrix[i][j - 1] * points[i]
        matrix[i][numerator_deg] = -values[i]
        for j in range(numerator_deg + 1, deg):
            matrix[i][j] = matrix[i][j - 1] * points[i]
    terms = [-(points[i] ** numerator_deg) for i in range(len(points))]
    # поиск коэффициентов и проверка их наличия
    coefficients = vanilla_gauss(matrix, terms, gauss_error)
    if not coefficients:
        return None
    print('Коэффициенты числителя:', 1, *coefficients[denominator_deg::-1])
    print('Коэффициенты знаменателя:', *coefficients[:denominator_deg:-1])
    # вычисление значения числителя
    numerator_polynomial = 0
    point_power = 1
    for i in range(numerator_deg):
        numerator_polynomial += coefficients[i] * point_power
        point_power *= point
    numerator_polynomial += point_power * point
    # вычисление значения знаменателя
    denominator_polynomial = 0
    point_power = 1
    for i in range(numerator_deg, deg):
        denominator_polynomial += coefficients[i] * point_power
        point_power *= point
    return numerator_polynomial / denominator_polynomial


def test_function(x: float) -> float:
    return (x**3 - 2 * x**2 + x - 3) / (4 * x**2 - 5 * x + 5)


def main():
    n = 5
    point = 1.5
    points = [i for i in range(n + 1)]
    values = [test_function(p) for p in points]
    print('Точка интерполяции:', point)
    function_value = test_function(point)
    print('Значение функции:', function_value)
    interpolation_value = ratio_interpolation(point, points, values, 3, 2)
    print('Значение интерполяции:', interpolation_value)
    print('Абсолютная точность:', abs(function_value - interpolation_value))


if __name__ == '__main__':
    main()
