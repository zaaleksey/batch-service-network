from dataclasses import dataclass
from random import expovariate


@dataclass()
class Clock:
    current: float = 0
    arrival: float = 0
    service_start: float = float('inf')
    leaving: float = float('inf')

    def update_arrival_time(self, lambda0: float) -> None:
        self.arrival += expovariate(lambda0)

    @property
    def time_of_next_event(self):
        return min(self.arrival, self.service_start, self.leaving)
