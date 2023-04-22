from params import Params
from progress.bar import ConsoleProgressBar
from route.routing import get_links_by_theta
from simulation_modal.simulation import Simulation, get_system_with_min_queue_len, get_system_with_max_mu

if __name__ == '__main__':
    # lambda0 = .8
    # servers_count = 7
    # mu = [1.1, 1.2, 1.5, 1.3, 1.2, 1.1, 1.4]
    # batch = [3, 2, 3, 2, 3, 1, 3]
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
    # lambda0 = .8
    # servers_count = 5
    # mu = [1.2, 1.3, 1.5, 1.4, 1.3]
    # batch = [2, 3, 2, 2, 2]
    # theta = [
    #     [.0, .3, .4, .0, .0, .3],
    #     [.3, .0, .2, .2, .3, .0],
    #     [.2, .3, .0, .3, .1, .1],
    #     [.3, .0, .2, .0, .3, .2],
    #     [.4, .0, .2, .0, .0, .4],
    #     [.5, .1, .2, .0, .2, .0]
    # ]

    lambda0 = .8
    servers_count = 6
    mu = [1., 1., 1.5, 1.3, 1.2, 1.1]
    batch = [1, 2, 1, 2, 3, 1]
    theta = [
        [.0, .2, .19, .18, .2, .0, .23],
        [.17, .0, .2, .23, .0, .19, .21],
        [.2, .21, .0, .17, .2, .0, .22],
        [.19, .0, .2, .0, .17, .21, .23],
        [.2, .2, .0, .19, .0, .21, .2],
        [.21, .19, .2, .0, .2, .0, .2],
        [.2, .23, .21, .19, .0, .17, .0]
    ]

    links = get_links_by_theta(theta)

    time = 1_000_000
    params = Params(mu=mu, lambda0=lambda0, systems_count=servers_count, batch=batch, links=links)

    bar1 = ConsoleProgressBar("Progress: ")
    model = Simulation(params=params, progress_bar=bar1)
    statistics = model.run(simulation_time=time)
    print(statistics, "\n")

    bar2 = ConsoleProgressBar("Progress (min queue len): ")
    model_with_control_queue_len = Simulation(params=params, progress_bar=bar2,
                                              with_control=True, control=get_system_with_min_queue_len)
    statistics_with_control_queue_len = model_with_control_queue_len.run(simulation_time=time)
    print(statistics_with_control_queue_len, "\n")

    # bar3 = ConsoleProgressBar("Progress (max mu): ")
    # model_with_control_max_mu = Simulation(params=params, progress_bar=bar3,
    #                                        with_control=True, control=get_system_with_max_mu)
    # statistics_with_control_max_mu = model_with_control_max_mu.run(simulation_time=time)
    # print(statistics_with_control_max_mu)
