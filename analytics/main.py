from analytics.solve import solve_M
from analytics.stat_func import *


def calculate_statistics_non_optimal(_L, _lambda0, _mu, _b, _theta):
    omega = get_omega(_L, _theta)
    print("omega:", omega)
    print("sum omega:", sum(omega))

    lambdas = get_lambdas(_L, _lambda0, omega)
    print("lambdas:", lambdas)

    psi = get_psi(_L, _b, lambdas, _mu)
    print("psi:", psi)

    print(check_psi(psi))

    M = solve_M(_L, lambdas, _mu, _b)
    print("M:", M)

    u = get_u(_L, lambdas, _b, M)
    print("u:", u)
    print(sorted(list(map(lambda item: (u.index(item), item), u)), key=lambda item: item[1]))

    tau = get_tau(_L, _lambda0, lambdas, u)
    print("tau:", tau)


if __name__ == '__main__':
    # L = 5
    # lambda0 = .8
    # mu = np.array([1.2, 1.3, 1.5, 1.4, 1.3])
    # b = np.array([2, 3, 2, 2, 2])
    #
    # Theta = np.array([
    #     [.0, .3, .4, .0, .0, .3],
    #     [.3, .0, .2, .2, .3, .0],
    #     [.2, .3, .0, .3, .1, .1],
    #     [.3, .0, .2, .0, .3, .2],
    #     [.4, .0, .2, .0, .0, .4],
    #     [.5, .1, .2, .0, .2, .0]
    # ])

    lambda0 = .8
    L = 7
    mu = np.array([1.1, 1.2, 1.5, 1.3, 1.2, 1.1, 1.4])
    b = np.array([3, 2, 3, 2, 3, 1, 3])
    Theta = np.array([
        [.0, .3, .0, .0, .4, .0, .0, .3],
        [.3, .0, .2, .2, .0, .1, .0, .2],
        [.2, .0, .0, .2, .3, .0, .3, .0],
        [.2, .0, .0, .0, .3, .2, .2, .1],
        [.0, .2, .0, .3, .0, .2, .3, .0],
        [.0, .3, .2, .0, .2, .0, .2, .1],
        [.4, .0, .2, .0, .0, .1, .0, .3],
        [.3, .0, .1, .2, .0, .1, .3, .0]
    ])

    calculate_statistics_non_optimal(L, lambda0, mu, b, Theta)
