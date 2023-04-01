class Statistics:
    def __init__(self) -> None:
        self.demands_in_network: list = []
        self.served_demands: list = []
        self.total_demands: int = 0
        self.demands_number: int = 0
        self.avg_response_time: float = .0
        self.avg_time_in_queue: float = .0
        self.avg_time_on_servers: float = .0
        self.avg_time_on_systems: float = .0

    def calculate_statistics(self) -> None:
        self.demands_number = len(self.served_demands)

        if self.demands_number == 0:
            return

        demands_in_queues_times = []
        demands_in_servers_times = []
        demands_in_systems_times = []
        demands_in_network_times = []
        for demand in self.served_demands:
            # рассчет для очереди
            time_in_queue_for_demand = 0
            for pair in zip(demand.service_start_times, demand.arrival_in_queue_times):
                time_in_queue_for_demand += (pair[0] - pair[1])
            demands_in_queues_times.append(time_in_queue_for_demand / len(demand.service_start_times))

            # рассчет для прибора
            time_in_server_for_demand = 0
            for pair in zip(demand.service_end_times, demand.service_start_times):
                time_in_server_for_demand += (pair[0] - pair[1])
            demands_in_servers_times.append(time_in_server_for_demand / len(demand.service_end_times))

            # рассчет для системы
            time_in_system_for_demand = 0
            for pair in zip(demand.service_end_times, demand.arrival_in_queue_times):
                time_in_system_for_demand += (pair[0] - pair[1])
            demands_in_systems_times.append(time_in_system_for_demand / len(demand.service_end_times))

            # рассчет для сети
            demands_in_network_times.append(demand.leaving_from_network_time - demand.arrival_in_network_time)

        self.avg_time_in_queue = sum(demands_in_queues_times) / len(demands_in_queues_times)
        self.avg_time_on_servers = sum(demands_in_servers_times) / len(demands_in_servers_times)
        self.avg_time_on_systems = self.avg_time_in_queue + self.avg_time_on_servers
        self.avg_response_time = sum(demands_in_network_times) / len(demands_in_network_times)
        # self.avg_response_time = sum(demands_in_systems_times) / len(demands_in_systems_times)

    def __str__(self) -> str:
        return f"\n{self.total_demands=}" \
               f"\n{self.demands_number=}" \
               f"\n{self.avg_time_in_queue=}" \
               f"\n{self.avg_time_on_servers=}" \
               f"\n{self.avg_time_on_systems=}" \
               f"\n{self.avg_response_time=}"
