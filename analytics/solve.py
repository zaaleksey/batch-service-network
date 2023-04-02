# Решение уравнения методом Ньютона (самописный)
def solve_M(L, lambdas, mu, b, eps=0.00001):
    def f(x, lambda_i, mu_i, b_i):
        return x ** (b_i + 1) - (x ** b_i) * (lambda_i + mu_i) + (lambda_i ** b_i) * mu_i

    def diff_f(x, lambda_i, mu_i, b_i):
        return (b_i + 1) * (x ** b_i) - b_i * (x ** (b_i - 1)) * (lambda_i + mu_i)

    def calculate(lambda_i, mu_i, b_i):
        a = (b_i * (lambda_i + mu_i)) / (b_i + 1)
        x1 = a
        x0 = x1 + 2 * eps
        while abs(x0 - x1) > eps:
            x1 = x0
            x0 = x0 - (f(x0, lambda_i, mu_i, b_i) / diff_f(x0, lambda_i, mu_i, b_i))

        return x1

    return [calculate(lambdas[i], mu[i], b[i]) for i in range(L)]
