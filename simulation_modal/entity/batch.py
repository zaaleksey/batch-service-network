from .demand import Demand
from .exception.batch_size_exception import BatchSizeException


class Batch:
    def __init__(self, size: int) -> None:
        self.size = size
        self.demands = None

    def form(self, demands: list[Demand]) -> None:
        if len(demands) != self.size:
            raise BatchSizeException

        self.demands = demands

    def clear(self) -> None:
        self.demands = None

    def __str__(self) -> str:
        return f"{self.demands}"
