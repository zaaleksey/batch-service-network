import logging
import random

from entity.clock import Clock
from entity.source import Source
from entity.system import System
from params import Params
from progress.bar import ProgressBar
from route.routing import Routing
from statistics import Statistics

logging.basicConfig(filename="logging.log", level=logging.DEBUG, filemode="w")


class Simulation:

    def __init__(self, params: Params, progress_bar: ProgressBar):
        self._params = params
        self._bar = progress_bar

        self._times = Clock()
        self._times.update_arrival_time(params.lambda0)

        self._source = Source(params.lambda0)
        self._systems = [self._source, *[System(params.mu[i], params.batch[i]) for i in range(params.systems_count)]]

        self._routing = Routing(params.links)

        self._demands_in_network = []
        self._served_demands = []
        self._total_demands = 0

    def run(self, simulation_time: int) -> Statistics:
        statistics = Statistics()
        while self._times.current <= simulation_time:
            self._times.current = self._times.time_of_next_event
            self._bar.update_progress(self._times.current, simulation_time)

            if self._times.current == self._times.arrival:
                self._demand_arrival()
                continue
            if self._times.current == self._times.service_start:
                self._demands_service_start()
                continue
            if self._times.current == self._times.leaving:
                self._demands_service_end()
                continue

        statistics.calculate_statistics(self._served_demands, self._total_demands)
        return statistics

    def _demand_arrival(self) -> None:
        self._total_demands += 1
        demand = self._source.create_demand(self._times.current)
        self._demands_in_network.append(demand)
        target_system = random.choices(
            # список смежных систем с источником
            population=list(map(lambda target: target.id, self._routing.map[0])),
            # список вероятностей переходов из источника
            weights=list(map(lambda target: target.probability, self._routing.map[0]))
        )[0]

        self._times.service_start = self._times.current
        self._systems[target_system].queue.append(demand)
        logging.debug(
            f"[ARRIVAL {self._times.current}] Demand with {demand.id} id added to queue in {target_system} system")
        self._times.update_arrival_time(self._source.lambda0)

    def _demands_service_start(self) -> None:
        leavings_times = []
        for system in self._systems[1:]:

            success = system.try_occupy(self._times.current)

            if success:
                logging.debug(f"[SERVICE {self._times.current}] System {system.id} start service batch {system.batch}")
                leavings_times.append(system.end_service_time)

        if leavings_times:
            self._times.leaving = min(leavings_times)
        elif list(map(lambda s: s.end_service_time, filter(lambda s: not s.is_free, self._systems[1:]))):
            self._times.leaving = min(map(lambda s: s.end_service_time, filter(lambda s: not s.is_free, self._systems[1:])))

        self._times.service_start = float('inf')

    def _demands_service_end(self) -> None:
        system = None
        min_leave_time = float("inf")
        for s in self._systems[1:]:

            if s.end_service_time < min_leave_time and not s.is_free:
                min_leave_time = s.end_service_time
                system = s

        demands = system.batch.demands
        logging.debug(f"[FREE {self._times.current}] Demands {demands} leaved system {system.id} / {system.queue}")
        system.to_free()

        system_id = self._systems.index(system)
        for demand in demands:
            target_system = random.choices(
                population=list(map(lambda target: target.id, self._routing.map[system_id])),
                weights=list(map(lambda target: target.probability, self._routing.map[system_id]))
            )[0]

            if target_system == 0:
                logging.debug(f"\t[LEAVING] Demand with id {demand.id} leaved network")
                demand.leaving_time = self._times.current
                self._demands_in_network.remove(demand)
                self._served_demands.append(demand)
            else:
                logging.debug(f"\t[JUMP] Demand with id {demand.id} arrived in system {target_system}")
                self._systems[target_system].queue.append(demand)
                if self._systems[target_system].can_occupy:
                    self._times.service_start = self._times.current

        self._times.leaving = float("inf")
        self._times.service_start = self._times.current
