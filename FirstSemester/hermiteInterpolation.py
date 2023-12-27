from typing import List


TARGET_POINT = 1

TARGET_FUNCTION_TABLE = [
    [],
    [],
    []
]


# TODO: когда-нибудь закончить
def hermite(point: float, func_table: List[List[float]],
            precision=10e-5) -> float:
    deg = len(func_table[0]) - 1
    # создание и инициализация таблицы разделённых разностей
    diff_table = [[0] * (deg + 2 - i) for i in range(deg + 1)]
    for i in range(deg + 1):
        for j in range(2):
            diff_table[i][j] = func_table[j][i]
    # вычисление таблицы разделённых разностей
    line_length = deg
    for j in range(deg + 2):
        for i in range(line_length):
            if abs(diff_table[i][0] - diff_table[i + j + 1][0]) >= precision:
                diff_table[i][j] = (
                    (diff_table[i][j - 1] - diff_table[i + 1][j - 1]) /
                    (diff_table[i][0] - diff_table[i + j + 1][0])
                )
            else:

                return 0
        line_length -= 1
    # вычисление интерполяционного многочлена Эрмита
    interpolation_polynomial = 0
    basis_polynomial = 1
    for i in range(deg + 1):
        interpolation_polynomial += basis_polynomial * diff_table[0][i + 1]
        basis_polynomial *= point - func_table[0][i]
    return interpolation_polynomial


def main():
    hermite(TARGET_POINT, TARGET_FUNCTION_TABLE)


if __name__ == '__main__':
    main()
