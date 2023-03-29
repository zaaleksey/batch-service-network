class Statistics:
    def __init__(self) -> None:
        self.total_demands: int = 0
        self.demands_number: int = 0
        self.avg_response_time: float = .0
        self.avg_time_in_queue: float = .0
        self.avg_time_on_servers: float = .0

    def calculate_statistics(self, demands: list, total_demands: int) -> None:
        self.total_demands = total_demands
        self.demands_number = len(demands)

        if self.demands_number == 0:
            return

        for demand in demands:
            self.avg_response_time += (demand.leaving_time - demand.arrival_time)
            self.avg_time_in_queue += (demand.service_start_time - demand.arrival_time)
            self.avg_time_on_servers += (demand.leaving_time - demand.service_start_time)
        self.avg_response_time /= self.demands_number
        self.avg_time_in_queue /= self.demands_number
        self.avg_time_on_servers /= self.demands_number

    def __str__(self) -> str:
        return f"\n{self.total_demands=}" \
               f"\n{self.demands_number=}" \
               f"\n{self.avg_response_time=}" \
               f"\n{self.avg_time_in_queue=}" \
               f"\n{self.avg_time_on_servers=}"
