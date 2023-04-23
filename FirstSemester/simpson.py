import numpy as np


def _iteration(func, start, sum0, sum1, sum2, step, frequency):
    frequency *= 2
    step /= 2
    sum2 += sum1
    sum1 = sum([func(start + step * i) for i in np.arange(1, frequency, 2)])
    integral2 = step / 3 * (sum0 + 4 * sum1 + 2 * sum2)
    return frequency, step, sum2, sum1, integral2


def composite_simpson_rule(func, start, end, frequency=10000, precision=10e-9):
    """
        Функция возвращает значение интеграла функции func на интервале
        [start, end], вычисленное методом Симпсона с наперед заданной
        точностью precision. Частота дискретизации задается параметром
        frequency.
    """
    step = (end - start) / frequency
    sum0 = func(start) + func(end)
    sum1 = sum([func(start + step * i) for i in np.arange(1, frequency, 2)])
    sum2 = sum([func(start + step * i) for i in np.arange(0, frequency, 2)])
    integral1 = step / 3 * (sum0 + 4 * sum1 + 2 * sum2)

    frequency, step, sum2, sum1, integral2 = \
        _iteration(func, start, sum0, sum1, sum2, step, frequency)
    iterations = 0
    print(f'Шаг {iterations}:', abs(integral2 - integral1))
    while abs(integral2 - integral1) > precision:
        integral1 = integral2
        frequency, step, sum2, sum1, integral2 = \
            _iteration(func, start, sum0, sum1, sum2, step, frequency)
        iterations += 1
        print(f'Шаг {iterations}:', abs(integral2 - integral1))
    return integral2, iterations


def main():
    precise_value = 2
    n = int(input('Введите стартовое чётное число отрезков разбиения: '))
    while n % 2 != 0:
        print('Ошибка ввода!')
        n = int(input('Введите стартовое чётное число отрезков разбиения: '))
    p = (15 / 16) * float(input('Введите точность: '))

    target_value, iterations = \
        composite_simpson_rule(np.sin, 0, np.pi, frequency=n, precision=p)

    print('Количество шагов:', iterations)
    print('Ожидаемый результат:', precise_value)
    print('Результат вычислений:', target_value)
    print('Абсолютная точность:', abs(target_value - precise_value))


if __name__ == '__main__':
    main()
