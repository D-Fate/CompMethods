import numpy as np
from cauchyProblemSystem import solve_cauchy


IS_DEMO = True
TARGET_START, TARGET_END, TARGET_STEP = 0, 1, 0.1
TARGET_KSI = 1
TARGET_BOUNDARY_CONDITIONS = (
    (0, 1, -1),
    (1, 1, 6.25)
)
TARGET_PRECISION = 10e-5


def _target_func(x, u, v) -> np.ndarray:
    return np.array([
        u - v + np.exp(x) * (1 + x * x),
        u + v + np.exp(x) * x
    ])


def _f(u, v, right_boundary_conditions):
    alpha1, beta1, gamma1 = right_boundary_conditions
    return alpha1 * u + beta1 * v - gamma1


# TODO: когда-нибудь отрефакторить
def shooting_method(
        start, end, step, boundary_conditions, func, ksi0, precision=10e-5
):
    print('Пристрелка.')
    alpha0, beta0, gamma0 = boundary_conditions[0]
    u0 = ksi0
    v0 = (gamma0 - alpha0 * ksi0) / beta0
    _, u0, v0 = solve_cauchy(start, u0, v0, step, end, func, precision)
    f0 = _f(u0, v0, boundary_conditions[1])
    u_0 = u0
    v_0 = v0
    print('F =', f0)

    solved = 1
    i = 1
    while True:
        solved += 1
        i += 1
        ksi1 = float(input(f'ksi{i}\n>> '))
        u0 = ksi1
        v0 = (gamma0 - alpha0 * ksi1) / beta0
        _, u0, v0 = solve_cauchy(start, u0, v0, step, end, func, precision)
        f1 = _f(u0, v0, boundary_conditions[1])
        u_1 = u0
        v_1 = v0
        print('F =', f1)
        if f0 * f1 < 0:
            break
        f0 = f1
        u_0 = u_1
        v_0 = v_1
        ksi0 = ksi1
    print('Значение F изменило знак.')

    print('Автоматическая стрельба.')
    automatic_volleys = 0
    while True:
        solved += 1
        automatic_volleys += 1
        ksi_half = (ksi0 + ksi1) / 2
        u0 = ksi_half
        v0 = (gamma0 - alpha0 * ksi_half) / beta0
        _, u0, v0 = solve_cauchy(start, u0, v0, step, end, func, precision)
        f_half = _f(u0, v0, boundary_conditions[1])
        u_half = u0
        v_half = v0
        if f0 * f_half < 0:
            f1 = f_half
            u_1 = u_half
            v_1 = v_half
            ksi1 = ksi_half
        else:
            f0 = f_half
            u_0 = u_half
            v_0 = v_half
            ksi0 = ksi_half
        if abs(f0 - f1) < precision / 10 or abs(f0) < precision / 10:
            break

    print('Результаты.')
    print('Кол-во решенных задач Коши:', solved)
    print('Кол-во автоматических залпов:', automatic_volleys)
    print('F(ksi) = 0 при ksi =', ksi_half)
    print('Значение погрешности между финальными выстрелами:')
    print(f'Δu = {u_0 - u_1}\nΔv = {v_0 - v_1}')


def main():
    if IS_DEMO:
        print('Вводные данные.')
        print(f'(a, b) = ({TARGET_START}, {TARGET_END})\n'
              f'Начальный шаг h0 = {TARGET_STEP}\n'
              f'(alpha0, beta0, gamma0) = {TARGET_BOUNDARY_CONDITIONS[0]}\n'
              f'(alpha1, beta1, gamma1) = {TARGET_BOUNDARY_CONDITIONS[1]}\n'
              f'Точность eps = {TARGET_PRECISION}\n'
              f'ksi1 = {TARGET_KSI}')
        shooting_method(
            start=TARGET_START,
            end=TARGET_END,
            step=TARGET_STEP,
            boundary_conditions=TARGET_BOUNDARY_CONDITIONS,
            func=_target_func,
            ksi0=TARGET_KSI,
            precision=TARGET_PRECISION
        )
    else:
        a, b = tuple(map(
            float,
            input('Введите левую и правую границы отрезка (a, b) через пробел\n>> ')
            .split()
        ))
        print('Ввод граничных условий')
        alpha0, beta0, gamma0 = tuple(map(
            float,
            input('Введите alpha0, beta0, gamma0 через пробел\n>> ').split()
        ))
        alpha1, beta1, gamma1 = tuple(map(
            float,
            input('Введите alpha1, beta1, gamma1 через пробел\n>> ').split()
        ))
        h = float(input('Введите начальный шаг h0\n>> '))
        ksi0 = float(input(f'Введите начальную точку ksi\n>> '))
        precision = float(input('Введите желаемую точность eps\n>> '))
        shooting_method(
            start=a,
            end=b,
            step=h,
            boundary_conditions=(
                (alpha0, beta0, gamma0),
                (alpha1, beta1, gamma1)
            ),
            func=_target_func,
            ksi0=ksi0,
            precision=precision
        )


if __name__ == '__main__':
    main()
