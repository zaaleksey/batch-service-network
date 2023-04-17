from analytics.solve import solve_M
from analytics.stat_func import *


def get_optimal_psi(_L, _b):
    psi = np.zeros(_L)
    alpha = 1.505
    for i in range(_L):
        temp = (_b[i] ** _b[i]) / ((_b[i] + alpha) ** _b[i])
        psi[i] = (1 / alpha) * (1 - temp)

    return psi


def get_unbalanced_systems(_L, _psi, _optimal_psi, eps=.09):
    return [i + 1 for i in range(_L) if abs(_psi[i] - _optimal_psi[i]) > eps]


def optimization(_L, _lambda0, _optimal_psi, _mu, _b, _theta, eps=.09):
    omega = get_omega(_L, _theta)
    lambdas = get_lambdas(_L, _lambda0, omega)
    psi = get_psi(_L, _b, lambdas, _mu)

    if not all(check_psi(psi)):
        print("Коэффициент использования превышает 1")
        return

    while len(get_unbalanced_systems(_L, psi, _optimal_psi)) != 0:
        D = np.zeros((_L + 1, _L), dtype=float)
        for i in range(_L + 1):
            for j in range(_L):
                if abs(psi[j] - _optimal_psi[j]) > eps:
                    D[i][j] = abs(_optimal_psi[j] - psi[j])
        # print("D:\n", D)

        for i in range(_theta.shape[0]):
            for j in range(1, _theta.shape[1]):
                if D[i][j - 1] != 0:
                    _theta[i][j] *= ((sum(D[i])) / D[i][j - 1])

        # print("\n_theta\n", _theta)
        # todo: провести нормализацию матрицы, элементы уходят в отрицательные значения
        for i in range(_theta.shape[0]):
            s = sum(_theta[i][1:])
            for j in range(1, _theta.shape[1]):
                _theta[i][j] /= s

        non_zero_count_in_row = []
        for i in range(_theta.shape[0]):
            count = 0
            for j in range(1, _theta.shape[1]):
                if _theta[i][j] != 0:
                    count += 1
            non_zero_count_in_row.append(count)

        for i in range(_theta.shape[0]):
            for j in range(1, _theta.shape[1]):
                if _theta[i][j] != 0:
                    _theta[i][j] -= (_theta[i][0] / non_zero_count_in_row[i])

        omega = get_omega(_L, _theta)
        lambdas = get_lambdas(_L, _lambda0, omega)
        psi = get_psi(_L, _b, lambdas, _mu)
        # print("omega: ", omega, " sum omega: ", sum(omega))
        # print("lambdas: ", lambdas)

        print("optimal_psi:\t", optimal_psi)
        print("psi:\t", psi)

        M = solve_M(_L, lambdas, _mu, _b)
        u = get_u(_L, lambdas, _b, M)
        tau = get_tau(_L, _lambda0, lambdas, u)
        # print("Характеристики при оптимизированной _theta")
        # print("M: ", M)
        # print("u: ", u)
        print("tau: ", tau)
        print("Итоговая матрица переходов:\n")
        print(_theta)
        for i, row in enumerate(_theta):
            print(f"check row {i + 1}: ", sum(row))


if __name__ == '__main__':
    L = 5
    lambda0 = .8
    mu = np.array([1.2, 1.3, 1.5, 1.4, 1.3])
    b = np.array([2, 3, 2, 2, 2])

    Theta = np.array([
        [.0, .3, .4, .0, .0, .3],
        [.3, .0, .2, .2, .3, .0],
        [.2, .3, .0, .3, .1, .1],
        [.3, .0, .2, .0, .3, .2],
        [.4, .0, .2, .0, .0, .4],
        [.5, .1, .2, .0, .2, .0]
    ])

    optimal_psi = get_optimal_psi(L, b)
    optimization(L, lambda0, optimal_psi, mu, b, Theta)
