from demand import Demand


class Source:

    def __init__(self, lambda0: float):
        self.id = 0
        self.lambda0 = lambda0

    def create_demand(self, arrival_time: float) -> Demand:
        return Demand(arrival_time)
