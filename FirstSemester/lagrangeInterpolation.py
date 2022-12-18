from math import factorial


def lagrange(point: float, x: list or tuple, y: list or tuple) -> float:
    """
        Функция возвращает значение интерполяционного многочлена Лагранжа в
        точке point. Многочлен задаётся массивами x и y узловых точек и
        значений функции в узловых точках соответственно.
    """
    interpolation_polynomial = 0
    for i in range(len(x)):
        basis_polynomial = 1
        for j in range(0, i):
            basis_polynomial *= (point - x[j]) / (x[i] - x[j])
        for j in range(i + 1, len(y)):
            basis_polynomial *= (point - x[j]) / (x[i] - x[j])
        interpolation_polynomial += y[i] * basis_polynomial
    return interpolation_polynomial


if __name__ == '__main__':
    # ввод степени
    deg = int(input('Введите степень многочлена: '))
    while deg < 1:
        print('Степень многочлена должна быть натуральной!')
        deg = int(input('Повторите ввод: '))

    # ввод узлов
    points = tuple(
        map(float, input('Введите узловые точки через пробел: ').split())
    )
    while len(points) != deg + 1:
        print('Количество узловых точек не соответствует введенной степени.')
        points = tuple(map(float, input('Повторите ввод: ').split()))

    # ввод значений в узлах
    values = tuple(
        map(float, input('Введите значения в точках через пробел: ').split())
    )
    while len(values) != deg + 1:
        print('Количество значений не соответствует введенной степени.')
        values = tuple(map(float, input('Повторите ввод: ').split()))

    # ввод точки интерполяции
    point = float(input('Введите точку интерполяции: '))

    # вывод значения многочлена Лагранжа в точке интерполяции
    print("Значение в точке интерполяции:", lagrange(point, points, values))

    # ввод константы для расчета погрешности
    error_const = float(input('Введите значение константы M: '))

    # расчет погрешности
    error = error_const
    for p in points:
        error *= point - p
    error /= factorial(deg + 1)

    # вывод погрешности
    print('Погрешность интерполяции:', error)
