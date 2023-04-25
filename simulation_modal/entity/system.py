from random import expovariate, randrange

from .batch import Batch
from .demand import Demand


class System:
    __COUNT = 0

    def __init__(self, mu: float, batch: int) -> None:
        System.__COUNT += 1
        self.id = System.__COUNT

        self.queue = []
        self.batch = Batch(batch)
        self.mu = mu
        self.is_free = True
        self.end_service_time = float('-inf')

        self.service_times_for_demands = []

    def try_occupy(self, current_time: float) -> bool:
        if not self.can_occupy:
            return False

        self.is_free = False
        self.batch.form([self.queue.pop(randrange(len(self.queue))) for _ in range(self.batch.size)])
        for demand in self.batch.demands:
            demand.service_start_times.append(current_time)

        self.end_service_time = current_time + expovariate(self.mu)
        return True

    def add_to_queue(self, demand: Demand, current_time: float) -> None:
        demand.arrival_in_queue_times.append(current_time)
        self.queue.append(demand)

    def to_free(self, current_time: float) -> None:
        self.is_free = True
        for demand in self.batch.demands:
            demand.service_end_times.append(current_time)
            self.service_times_for_demands.append(demand.service_end_times[-1] - demand.arrival_in_queue_times[-1])

        self.batch.clear()
        self.end_service_time = float('-inf')

    @property
    def can_occupy(self):
        return self.is_free and len(self.queue) >= self.batch.size

    @property
    def queue_len(self):
        return len(self.queue)

    @classmethod
    def reset_counter(cls):
        System.__COUNT = 0
