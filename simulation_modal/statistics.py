class Statistics:
    def __init__(self) -> None:
        self.demands_in_network: list = []
        self.served_demands: list = []
        self.total_demands: int = 0
        self.demands_number: int = 0
        self.avg_response_time: float = .0

        self.u: list = []

    def calculate_statistics(self, systems) -> None:
        self.demands_number = len(self.served_demands)

        if self.demands_number == 0:
            return

        self.u = list(map(lambda system: sum(system.service_times_for_demands) / len(system.service_times_for_demands), systems))
        self.u = sorted(list(map(lambda item: (self.u.index(item), item), self.u)), key=lambda item: item[1])

        demands_in_network_times = []
        for demand in self.served_demands:
            # рассчет для сети
            demands_in_network_times.append(demand.leaving_from_network_time - demand.arrival_in_network_time)

        self.avg_response_time = sum(demands_in_network_times) / len(demands_in_network_times)

    def __str__(self) -> str:
        return f"\n{self.total_demands=}" \
               f"\n{self.demands_number=}" \
               f"\n{self.avg_response_time=}" \
               f"\n{self.u=}"
