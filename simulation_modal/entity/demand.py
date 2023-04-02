class Demand:

    __COUNT = 0

    def __init__(self, arrival_time: float) -> None:
        self.id = Demand.__COUNT
        self.arrival_in_network_time = arrival_time
        self.arrival_in_queue_times = []
        self.service_start_times = []
        self.service_end_times = []
        self.leaving_from_network_time = None

        Demand.__COUNT += 1

    @staticmethod
    def _reset_counter():
        Demand.__COUNT = 0

    def __str__(self):
        return f"{self.id}"

    def __repr__(self):
        return str(self)
