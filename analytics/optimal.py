from analytics.solve import solve_M
from analytics.stat_func import *


def get_optimal_psi(_L, _b):
    psi = np.zeros(_L)
    alpha = 1.505
    for i in range(_L):
        temp = (_b[i] ** _b[i]) / ((_b[i] + alpha) ** _b[i])
        psi[i] = (1 / alpha) * (1 - temp)

    return psi


def get_unbalanced_systems(_L, _psi, _optimal_psi):
    return [i + 1 for i in range(_L) if _psi[i] > _optimal_psi[i]]


def optimization(_L, _lambda0, _optimal_psi, _mu, _b, _theta):
    omega = get_omega(_L, _theta)
    lambdas = get_lambdas(_L, _lambda0, omega)
    psi = get_psi(_L, _b, lambdas, _mu)
    M = solve_M(L, lambdas, mu, b)
    u = get_u(L, lambdas, b, M)
    tau = get_tau(L, lambda0, lambdas, u)
    print("Оптимальная psi: ", optimal_psi)
    print("Начальная psi: ", psi)
    print("Начальное tau: ", tau)

    if not all(check_psi(psi)):
        print("Коэффициент использования превышает 1")
        return

    # При наличии только одной неоптимальной psi, алгоритм не работает и не меняет маршрутную матриц
    while len(get_unbalanced_systems(_L, psi, _optimal_psi)) > 1:
        D = np.zeros((_L + 1, _L), dtype=float)
        for i in range(_L + 1):
            for j in range(_L):
                if psi[j] > _optimal_psi[j]:
                    D[i][j] = abs(_optimal_psi[j] - psi[j])

        for i in range(_theta.shape[0]):
            for j in range(1, _theta.shape[1]):
                if D[i][j - 1] != 0:
                    _theta[i][j] *= (D[i][j - 1] / sum(D[i]))

        for i in range(_theta.shape[0]):
            s = sum(_theta[i])
            for j in range(_theta.shape[1]):
                _theta[i][j] /= s

        omega = get_omega(_L, _theta)
        lambdas = get_lambdas(_L, _lambda0, omega)
        psi = get_psi(_L, _b, lambdas, _mu)

        M = solve_M(_L, lambdas, _mu, _b)
        u = get_u(_L, lambdas, _b, M)
        tau = get_tau(_L, _lambda0, lambdas, u)

        print("D:\n", D, "\n")
        print("Оптимальная psi: ", optimal_psi)
        print("psi: ", psi)
        print("Матрица переходов:\n")
        print(_theta)
        print("tau: ", tau)
        for i, row in enumerate(_theta):
            print(f"check row {i + 1}: ", sum(row))


if __name__ == '__main__':
    # L = 5
    # lambda0 = .8
    # mu = np.array([1.1, .85, .9, 1.2, 1.2])
    # b = np.array([1, 2, 1, 2, 1])
    #
    # Theta = np.array([
    #     [.0, .3, .4, .0, .0, .3],
    #     [.3, .0, .3, .2, .2, .0],
    #     [.2, .3, .0, .3, .1, .1],
    #     [.2, .0, .3, .0, .3, .2],
    #     [.4, .0, .3, .0, .0, .3],
    #     [.5, .1, .3, .0, .1, .0]
    # ])

    lambda0 = .8
    L = 6
    mu = np.array([1., 1., 1.5, 1.3, 1.2, 1.1])
    b = np.array([1, 2, 1, 2, 3, 1])
    Theta = np.array([
        [.0, .2, .19, .18, .2, .0, .23],
        [.17, .0, .2, .23, .0, .19, .21],
        [.2, .21, .0, .17, .2, .0, .22],
        [.19, .0, .2, .0, .17, .21, .23],
        [.2, .2, .0, .19, .0, .21, .2],
        [.21, .19, .2, .0, .2, .0, .2],
        [.2, .23, .21, .19, .0, .17, .0]
    ])

    optimal_psi = get_optimal_psi(L, b)
    optimization(L, lambda0, optimal_psi, mu, b, Theta)
