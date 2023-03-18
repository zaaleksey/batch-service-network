from random import expovariate, randrange

from .batch import Batch


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

        self.end_service_time = current_time + expovariate(self.batch.size * self.mu)
        return True

    def to_free(self) -> None:
        self.is_free = True
        self.batch.clear()
        self.end_service_time = float('-inf')

    @property
    def can_occupy(self):
        return self.is_free and len(self.queue) >= self.batch.size
