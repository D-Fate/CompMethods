from newtonInterpolation import newton
from math import sin, factorial
from random import uniform


TARGET_POINT = 3.14159265358
TARGET_POINTS = [2.8, 3, 3.1, 3.3]


def newton_demo(f, error_const, deg, point=None, points=None, label=''):
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
    newton_res = newton(point, points, values)
    function_res = f(point)
    # расчет погрешности
    error = error_const
    for p in points:
        error *= point - p
    error /= factorial(deg + 1)
    # вывод
    print('Точка интерполяции:', point)
    print('Значение интерполяции:', newton_res)
    print('Значение функции:', function_res)
    print('Точность:', abs(function_res - newton_res), '<=', abs(error))


if __name__ == '__main__':
    newton_demo(f=lambda x: x ** 3, error_const=0, deg=3,
                point=TARGET_POINT, points=TARGET_POINTS, label='y = x^3')
    print()
    newton_demo(f=sin, error_const=1, deg=4,
                point=TARGET_POINT, points=TARGET_POINTS, label='y = sin(x)')
