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

    def try_occupy(self, current_time: float) -> bool:
        if not self.can_occupy:
            return False

        self.is_free = False
        self.batch.form([self.queue.pop(randrange(len(self.queue))) for _ in range(self.batch.size)])
        for demand in self.batch.demands:
            demand.service_start_times.append(current_time)

        # self.end_service_time = current_time + expovariate(self.batch.size * self.mu)
        services_time = sum([expovariate(self.mu) for _ in range(self.batch.size)])
        self.end_service_time = current_time + services_time
        return True

    def add_to_queue(self, demand: Demand, current_time: float) -> None:
        demand.arrival_in_queue_times.append(current_time)
        self.queue.append(demand)

    def to_free(self, current_time: float) -> None:
        self.is_free = True
        for demand in self.batch.demands:
            demand.service_end_times.append(current_time)
        self.batch.clear()
        self.end_service_time = float('-inf')

    @property
    def can_occupy(self):
        return self.is_free and len(self.queue) >= self.batch.size
