from batch_size_exception import BatchSizeException
from demand import Demand


class Batch:
    def __init__(self, size: int):
        self.size = size
        self.demands = None

    def form(self, demands: list[Demand]):
        if len(demands) != self.size:
            raise BatchSizeException

        self.demands = demands

    def clear(self):
        self.demands = None
