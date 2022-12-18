from FirstSemester.lagrangeInterpolation import lagrange
from math import sin, factorial
from random import uniform


TARGET_POINT = None
TARGET_POINTS = None


def lagrange_test(f, error_const, deg, point=None, points=None, label=''):
    if label:
        print(label)
    # подготовка значений для расчета интерполяции
    if not points:
        random_float = uniform(-10, 10)
        step = 0.2
        points = [random_float + step * i for i in range(deg + 1)]
    if not point:
        point = uniform(min(points), max(points))
    values = [f(p) for p in points]
    # расчет значений интерполяции и функции
    lagrange_res = lagrange(point, points, values)
    function_res = f(point)
    # расчет погрешности
    error = error_const
    for p in points:
        error *= point - p
    error /= factorial(deg + 1)
    # вывод
    print('Точка интерполяции:', point)
    print('Значение интерполяции:', lagrange_res)
    print('Значение функции:', function_res)
    print('Точность:', abs(function_res - lagrange_res), '<=', abs(error))


if __name__ == '__main__':
    lagrange_test(f=lambda x: x**3, error_const=0, deg=3, label='Тест x^3.')
    print()
    lagrange_test(f=sin, error_const=1, deg=4, label='Тест sin(x).')
