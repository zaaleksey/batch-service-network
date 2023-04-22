import logging
import random

from entity.clock import Clock
from entity.source import Source
from entity.system import System
from params import Params
from progress.bar import ProgressBar
from route.routing import Routing
from .statistics import Statistics

logging.basicConfig(filename="logging.log", level=logging.ERROR, filemode="w")


def get_system_with_min_queue_len(systems):
    ids_with_queue_len = dict(map(lambda system: (system.id, len(system.queue)), systems))
    return min(ids_with_queue_len, key=ids_with_queue_len.get)


def get_system_with_max_mu(systems):
    ids_with_mu = dict(map(lambda system: (system.id, system.mu), systems))
    return max(ids_with_mu, key=ids_with_mu.get)


class Simulation:

    def __init__(self, params: Params,
                 progress_bar: ProgressBar,
                 with_control: bool = False,
                 control=None):
        self.params = params
        self.bar = progress_bar
        self.with_control = with_control
        self.get_target_system = control

        self.times = Clock()
        self.times.update_arrival_time(params.lambda0)

        System.reset_counter()
        self.source = Source(params.lambda0)
        self.systems = [self.source, *[System(params.mu[i], params.batch[i]) for i in range(params.systems_count)]]

        self.routing = Routing(params.links)

        self.statistics = Statistics()

    def run(self, simulation_time: int) -> Statistics:
        while self.times.current <= simulation_time:
            self.times.current = self.times.time_of_next_event
            self.bar.update_progress(self.times.current, simulation_time)

            if self.times.current == self.times.arrival:
                self._demand_arrival()
                continue
            if self.times.current == self.times.service_start:
                self._demands_service_start()
                continue
            if self.times.current == self.times.leaving:
                self._demands_service_end()
                continue

        self.statistics.calculate_statistics(self.systems[1:])
        return self.statistics

    def _demand_arrival(self) -> None:
        self.statistics.total_demands += 1
        demand = self.source.create_demand(self.times.current)
        self.statistics.demands_in_network.append(demand)
        target_system = random.choices(
            # список смежных систем с источником
            population=list(map(lambda target: target.id, self.routing.map[0])),
            # список вероятностей переходов из источника
            weights=list(map(lambda target: target.probability, self.routing.map[0]))
        )[0]

        self.times.service_start = self.times.current
        self.systems[target_system].add_to_queue(demand, self.times.current)
        logging.debug(
            f"[ARRIVAL {self.times.current}] Demand with {demand.id} id added to queue in {target_system} system")
        self.times.update_arrival_time(self.source.lambda0)

    def _demands_service_start(self) -> None:
        for system in self.systems[1:]:

            success = system.try_occupy(self.times.current)
            if success:
                logging.debug(f"[SERVICE {self.times.current}] System {system.id} start service batch {system.batch}")

        end_service_times = list(map(lambda s: s.end_service_time, filter(lambda s: not s.is_free, self.systems[1:])))
        if end_service_times:
            self.times.leaving = min(end_service_times)

        self.times.service_start = float('inf')

    def _demands_service_end(self) -> None:
        system = None
        min_leave_time = float("inf")
        for s in self.systems[1:]:

            if s.end_service_time < min_leave_time and not s.is_free:
                min_leave_time = s.end_service_time
                system = s

        demands = system.batch.demands
        logging.debug(f"[FREE {self.times.current}] Demands {demands} leaved system {system.id} / {system.queue}")
        system.to_free(self.times.current)

        system_id = self.systems.index(system)
        for demand in demands:
            connected_systems_id = list(map(lambda target: target.id, self.routing.map[system_id]))
            connected_probabilities = list(map(lambda target: target.probability, self.routing.map[system_id]))
            target_system = random.choices(population=connected_systems_id, weights=connected_probabilities)[0]

            if target_system == 0:
                logging.debug(f"\t[LEAVING] Demand with id {demand.id} leaved network")
                demand.leaving_from_network_time = self.times.current
                self.statistics.demands_in_network.remove(demand)
                self.statistics.served_demands.append(demand)
            else:
                if self.with_control:
                    connected_systems_id.remove(0)
                    connected_systems = [system for system in self.systems if system.id in connected_systems_id]
                    target_system = self.get_target_system(connected_systems)

                logging.debug(f"\t[JUMP] Demand with id {demand.id} arrived in system {target_system}")
                self.systems[target_system].add_to_queue(demand, self.times.current)
                if self.systems[target_system].can_occupy:
                    self.times.service_start = self.times.current

        self.times.leaving = float("inf")
        self.times.service_start = self.times.current
