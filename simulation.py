import random

from entity.clock import Clock
from entity.source import Source
from entity.system import System
from params import Params
from progress.bar import ProgressBar
from route.routing import Routing


class Simulation:

    def __init__(self, params: Params, progress_bar: ProgressBar):
        self._params = params
        self._bar = progress_bar

        self._times = Clock()
        self._times.update_arrival_time(params.lambda0)

        self._source = Source(params.lambda0)
        self._systems = [System(params.mu[i], params.batch[i]) for i in range(params.systems_count)]

        self._routing = Routing(params.links)

        self._demand_in_network = []
        self._served_demand = []

    def run(self, simulation_time: int):
        while self._times.current <= simulation_time:
            self._times.current = self._times.time_of_next_event
            self._bar.update_progress(self._times.current, simulation_time)
            # log state?

            if self._times.current == self._times.arrival:
                self._demand_arrival(arrival_time=self._times.current)
                continue
            if self._times.current == self._times.service_start:
                self._demand_service_start()
                continue
            if self._times.current == self._times.leaving:
                self._demand_leaving()
                continue

    def _demand_arrival(self, arrival_time: float) -> None:
        demand = self._source.create_demand(arrival_time)
        target_system = random.choices(
            # список смежных систем с источником
            population=list(map(lambda target: target.id, self._routing.map[0])),
            # список вероятностей переходов из источника
            weights=list(map(lambda target: target.probability, self._routing.map[0]))
        )

        self._times.service_start = self._times.current
        self._systems[target_system - 1].queue.append(demand)
        print(f"[ARRIVAL {self._times.current}] Demand with {demand.id} id added to queue in {target_system} system")
        self._times.update_arrival_time(self._source.lambda0)

    def _demand_service_start(self) -> None:
        for system in self._systems:
            success = system.try_occupy(self._times.current)

            if success:
                print(f"[SERVICE {self._times.current}] System {system.id} start service batch {system.batch}")

        self._times.service_start = float('inf')

    def _demand_leaving(self) -> None:
        pass
