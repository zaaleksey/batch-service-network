class Demand:

    __COUNT = 0

    def __init__(self, arrival_time: float) -> None:
        self.id = Demand.__COUNT
        self.served = False
        self.arrival_time = arrival_time
        self.service_start_time = None
        self.leaving_time = None

        Demand.__COUNT += 1

    @staticmethod
    def _reset_counter():
        Demand.__COUNT = 0
