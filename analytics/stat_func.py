import numpy as np


def get_omega(L, Theta):
    omega = np.array([1 / (L + 1) for _ in range(L + 1)])
    for _ in range(10_000_000):
        omega = omega.dot(Theta)
    return omega


def get_lambdas(L, lambda0, omega):
    return np.array([(omega[i] / omega[0]) * lambda0 for i in range(1, L + 1)])


def get_psi(L, b, lambdas, mu):
    return np.array([lambdas[i] / (b[i] * mu[i]) for i in range(L)])


def check_psi(psi):
    return [True if elem < 1 else False for elem in psi]


def get_u(L, lambdas, b, M):
    return [(b[i] - 1) / (2 * lambdas[i]) + (1 / (M[i] - lambdas[i])) for i in range(L)]


def get_tau(L, lambda0, lambdas, u):
    return (1 / lambda0) * sum([lambdas[i] * u[i] for i in range(L)])
