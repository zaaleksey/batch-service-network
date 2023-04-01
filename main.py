from params import Params
from progress.bar import ConsoleProgressBar
from route.routing import get_links_by_theta
from simulation import Simulation

if __name__ == '__main__':
    # lambda0 = .5
    # servers_count = 7
    # mu = [.7, .7, .7, .7, .7, .7, .7]
    # batch = [3, 2, 3, 2, 3, 2, 3]
    # theta = [
    #     [.0, .3, .0, .0, .4, .0, .0, .3],
    #     [.3, .0, .2, .2, .0, .1, .0, .2],
    #     [.2, .0, .0, .2, .3, .0, .3, .0],
    #     [.2, .0, .0, .0, .3, .2, .2, .1],
    #     [.0, .2, .0, .3, .0, .2, .3, .0],
    #     [.0, .3, .2, .0, .2, .0, .2, .1],
    #     [.4, .0, .2, .0, .0, .1, .0, .3],
    #     [.3, .0, .1, .2, .0, .1, .3, .0]
    # ]
    lambda0 = .7
    servers_count = 5
    mu = [1.1, 1.2, 1.4, 1.3, 1.2]
    batch = [2, 3, 2, 1, 2]
    theta = [
        [.0, .3, .0, .0, .0, .7],
        [.3, .0, .2, .2, .3, .0],
        [.2, .3, .0, .3, .1, .1],
        [.3, .0, .2, .0, .3, .2],
        [.4, .0, .2, .0, .0, .4],
        [.5, .1, .2, .0, .2, .0]
    ]
    links = get_links_by_theta(theta)

    params = Params(mu=mu, lambda0=lambda0, systems_count=servers_count, batch=batch, links=links)
    bar = ConsoleProgressBar("Progress: ")

    model = Simulation(params=params, progress_bar=bar)

    # time = 1_000_000
    time = 500_000
    statistics = model.run(simulation_time=time)
    print(statistics)
