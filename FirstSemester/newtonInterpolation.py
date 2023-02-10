from math import factorial


def newton(point: float, x: list | tuple, y: list | tuple) -> float:
    """
        Функция возвращает значение интерполяционного многочлена Ньютона в
        точке point. Многочлен задаётся массивами x и y узловых точек и
        значений функции в узловых точках соответственно.
    """
    coefficients = list(y)
    for i in range(1, len(y)):
        for j in range(len(y) - 1, i - 1, -1):
            coefficients[j] = (coefficients[j] - coefficients[j - 1]) / \
                              (x[j] - x[j - i])
    interpolation_polynomial = 0
    basis_polynomial = 1
    for i in range(len(y)):
        print(f'Промежуточная сумма на {i}-й итерации: '
              f'{interpolation_polynomial}')
        interpolation_polynomial += basis_polynomial * coefficients[i]
        basis_polynomial *= point - x[i]
    return interpolation_polynomial


def main():
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
    print("Значение в точке интерполяции:", newton(point, points, values))

    # ввод константы для расчета погрешности
    error_const = float(input('Введите значение константы M: '))

    # расчет погрешности
    error = error_const
    for p in points:
        error *= point - p
    error /= factorial(deg + 1)

    # вывод погрешности
    print('Погрешность интерполяции:', error)


if __name__ == '__main__':
    main()
